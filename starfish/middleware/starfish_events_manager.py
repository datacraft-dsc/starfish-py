#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0


import logging
import os
import time
from datetime import datetime
from threading import Thread


from ocean_events_handler.event_handlers import accessSecretStore, lockRewardCondition
from ocean_utils.agreements.service_agreement import ServiceAgreement
from ocean_utils.agreements.service_agreement_template import ServiceAgreementTemplate
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.agreements.utils import get_sla_template
from ocean_events_handler.agreement_store.agreements import AgreementsStorage
from ocean_utils.did import id_to_did
from ocean_utils.did_resolver.did_resolver import DIDResolver
from ocean_keeper.web3_provider import Web3Provider

logger = logging.getLogger(__name__)


class StarfishAgreementRecord:

    def __init__(self, agreement_id, publisher, consumer, provider, did, condition_to_id):
        self.agreement_id = agreement_id
        self.publisher = publisher
        self.consumer = consumer
        self.provider = provider
        self.did = did
        self.condition_to_id = condition_to_id
        self.cond_state = {cond: 0 for cond in condition_to_id.keys()}
        self.created = int(datetime.now().timestamp())

    @property
    def completed(self):
        return len([1 for s in self.cond_state.values() if s >= 2]) == 3

    @property
    def missing_conditions(self):
        return {cond for cond, state in self.cond_state.items() if state < 2}

    def get_condition_id(self, cond):
        return self.condition_to_id.get(cond)

    def update_cond_state(self, cond, state):
        self.cond_state[cond] = state

    @property
    def report(self):
        return f'{self.agreement_id} -> {self.cond_state.items()}'


class StarfishEventsManager:
    """


    Manage the main keeper events listeners necessary for processing service agreements.

    on init
        if not db or not db schema -> create db and schema
        determine LAST_N_BLOCKS (allow setting from outside using an env var)
        read agreements from local database since LAST_N_BLOCKS
            keep set of completed/fulfilled (all conditions fulfilled) agreements to avoid reprocessing during event processing
            process events for unfulfilled agreements

    in watcher loop
        get AgreementCreated events since LAST_N_BLOCKS or LAST_PROCESSED_BLOCK whichever is larger
            try to overlap LAST_PROCESSED_BLOCK when grabbing events so we don't miss any events

    on new agreement (AgreementCreated event)
        save agreement to db
        init agreement conditions with unfulfilled status
        watch condition events
            on each condition event
                update agreement condition status


    """

    _instance = None

    EVENT_WAIT_TIMEOUT = 3600
    LAST_N_BLOCKS = 200

    def __init__(self, keeper, storage_path, account):
        self._keeper = keeper
        self._storage_path = storage_path
        self._account = account
        self._web3 = Web3Provider.get_web3()
        self._db = AgreementsStorage(self._storage_path)
        self._is_valid_callback = None

        self.known_agreement_ids = set()
        self.completed_ids = set()
        self.other_agreement_ids = set()

        # prepare condition names and events arguments dict
        sla_template = ServiceAgreementTemplate(template_json=get_sla_template())
        self.condition_names = [cond.name for cond in sla_template.conditions]
        self.event_to_arg_names = sla_template.get_event_to_args_map(self._keeper.contract_name_to_instance)

        db = self.db
        db.create_tables()
        # get largest block_number from db or `latest` if db has no data
        self.last_n_blocks = os.getenv('OCN_EVENTS_MONITOR_LAST_N_BLOCKS', self.LAST_N_BLOCKS)
        self.latest_block = self._web3.eth.blockNumber
        db_latest = db.get_latest_block_number() or self.latest_block
        self.latest_block = min(db_latest, self.latest_block)
        self.last_processed_block = 0
        logger.debug(f'starting events monitor: latest block number {self.latest_block}')

        self._monitor_is_on = False
        try:
            self._monitor_sleep_time = os.getenv('OCN_SQUID_EVENTS_MONITOR_TIME', 3)
        except ValueError:
            self._monitor_sleep_time = 3

        self._monitor_sleep_time = max(self._monitor_sleep_time, 3)

    @staticmethod
    def get_instance(keeper, storage_path, account):
        if not StarfishEventsManager._instance or StarfishEventsManager._instance.provider_account != account:
            StarfishEventsManager._instance = StarfishEventsManager(keeper, storage_path, account)

        return StarfishEventsManager._instance

    @property
    def db(self):
        return AgreementsStorage(self._storage_path)

    @property
    def provider_account(self):
        return self._account

    @property
    def is_monitor_running(self):
        return self._monitor_is_on

    def start_agreement_events_monitor(self, is_valid_callback=None):
        self._is_valid_callback = is_valid_callback

        if self._monitor_is_on:
            return

        logger.debug(f'Starting the agreement events monitor.')
        t = Thread(
            target=self.run_monitor,
            daemon=True,
        )
        self._monitor_is_on = True
        t.start()
        logger.debug('started the agreement events monitor')

    def stop_monitor(self):
        self._monitor_is_on = False
        self._is_valid_callback = None

    def process_pending_agreements(self, pending_agreements, conditions):
        logger.debug(f'processing pending agreements, there is {len(pending_agreements)} agreements to process.')
        for agreement_id in pending_agreements.keys():
            data = pending_agreements[agreement_id]
            did = data[0]
            consumer_address = data[5]
            block_number = data[6]
            unfulfilled_conditions = conditions[agreement_id].keys()
            self.process_condition_events(
                agreement_id,
                unfulfilled_conditions,
                did,
                consumer_address,
                block_number,
                new_agreement=False
            )

    def get_next_block_range(self):
        to_block = self._web3.eth.blockNumber
        if self.last_processed_block:
            block_range = self.last_processed_block - 1, to_block
        else:
            block_num = self.db.get_latest_block_number() or 0
            if block_num > to_block:
                block_num = to_block - self.last_n_blocks
            from_block = max(to_block - self.last_n_blocks, block_num)
            block_range = from_block, to_block

        logger.debug(f'next block range = {block_range}, latest block number: {to_block}')
        return block_range

    def do_first_check(self):
        db = self.db
        if not db.get_agreement_count():
            return

        block_num = db.get_latest_block_number()
        agreements, conditions = db.get_pending_agreements(block_num - self.last_n_blocks)
        self.process_pending_agreements(agreements, conditions)

    def run_monitor(self):
        try:
            self.do_first_check()
        except Exception as e:
            logger.debug(f'Error processing event: {str(e)}')

        while True:
            try:
                if not self._monitor_is_on:
                    return

                _from, _to = self.get_next_block_range()
                for event_log in self.get_agreement_events(_from, _to):
                    self._handle_agreement_created_event(event_log)

                self.last_processed_block = _to

            except Exception as e:
                logger.debug(f'Error processing event: {str(e)}')

            time.sleep(self._monitor_sleep_time)

    def get_last_block_number(self):
        return self.latest_block - 100

    def get_agreement_events(self, from_block, to_block):
        event_filter = self._keeper.escrow_access_secretstore_template.get_event_filter_for_agreement_created(
            self._account.address, from_block, to_block)
        logger.debug(f'getting event logs in range {from_block} to {to_block} for provider address {self._account.address}')
        logs = event_filter.get_all_entries(max_tries=5)
        # event_filter.uninstall()
        return logs

    def _handle_agreement_created_event(self, event, *_):
        if not event or not event.args:
            return

        if self._account.address != event.args["_accessProvider"]:
            logger.debug(f'agreement event not for my address {self._account.address}, event provider address {event.args["_accessProvider"]}')
            return
        agreement_id = None
        try:
            agreement_id = self._web3.toHex(event.args["_agreementId"])
            ids = self.db.get_agreement_ids()
            if ids:
                # logger.info(f'got agreement ids: #{agreement_id}#, ##{ids}##, \nid in ids: {agreement_id in ids}')
                if agreement_id in ids:
                    logger.debug(f'handle_agreement_created: skipping service agreement {agreement_id} '
                                 f'because it already been processed before.')
                    return

            logger.debug(f'Start handle_agreement_created (agreementId {agreement_id}): event_args={event.args}')

            did = id_to_did(event.args["_did"])

            unfulfilled_conditions = ['lockReward', 'accessSecretStore', 'escrowReward']
            self.process_condition_events(
                agreement_id, unfulfilled_conditions, did, event.args['_accessConsumer'],
                event.blockNumber, new_agreement=True
            )

            logger.debug(f'handle_agreement_created()  (agreementId {agreement_id}) -- '
                         f'done registering event listeners.')

        except Exception as e:
            logger.error(f'Error in handle_agreement_created (agreementId {agreement_id}): {e}', exc_info=1)

    def _last_condition_fulfilled(self, _, agreement_id, cond_name_to_id):
        # update db, escrow reward status to fulfilled
        # log the success of this transaction
        db = self.db
        for cond, _id in cond_name_to_id.items():
            state = self._keeper.condition_manager.get_condition_state(_id)
            db.update_condition_status(agreement_id, cond, state)

        logger.info(f'Agreement {agreement_id} is completed, all conditions are fulfilled.')

    def process_condition_events(self, agreement_id, conditions, did,
                                 consumer_address, block_number, new_agreement=True):

        # check the callback, if set then
        if self._is_valid_callback is not None:
            is_valid = self._is_valid_callback(did, agreement_id, self._account.address, consumer_address)
            if not is_valid:
                return

        ddo = DIDResolver(self._keeper.did_registry).resolve(did)
        service_agreement = ServiceAgreement.from_ddo(ServiceTypes.ASSET_ACCESS, ddo)
        condition_def_dict = service_agreement.condition_by_name
        price = service_agreement.get_price()
        if new_agreement:
            start_time = int(datetime.now().timestamp())
            self.db.record_service_agreement(
                agreement_id, ddo.did, service_agreement.service_definition_id, price,
                ddo.metadata['base'].get('encryptedFiles'), consumer_address, start_time,
                block_number, ServiceTypes.ASSET_ACCESS,
                service_agreement.condition_by_name.keys()
            )

        condition_ids = service_agreement.generate_agreement_condition_ids(
            agreement_id=agreement_id,
            asset_id=ddo.asset_id,
            consumer_address=consumer_address,
            publisher_address=ddo.publisher,
            keeper=self._keeper
        )
        cond_order = ['accessSecretStore', 'lockReward', 'escrowReward']
        cond_to_id = {cond_order[i]: _id for i, _id in enumerate(condition_ids)}
        for cond in conditions:

            if cond == 'lockReward':
                self._keeper.lock_reward_condition.subscribe_condition_fulfilled(
                    agreement_id,
                    max(condition_def_dict['lockReward'].timeout, self.EVENT_WAIT_TIMEOUT),
                    lockRewardCondition.fulfillAccessSecretStoreCondition,
                    (agreement_id, ddo.did, service_agreement, consumer_address,
                     self._account, condition_ids[0]),
                    from_block=block_number
                )
            elif cond == 'accessSecretStore':
                self._keeper.access_secret_store_condition.subscribe_condition_fulfilled(
                    agreement_id,
                    max(condition_def_dict['accessSecretStore'].timeout, self.EVENT_WAIT_TIMEOUT),
                    accessSecretStore.fulfillEscrowRewardCondition,
                    (agreement_id, service_agreement, price, consumer_address, self._account,
                     condition_ids, condition_ids[2]),
                    from_block=block_number
                )
            elif cond == 'escrowReward':
                self._keeper.escrow_reward_condition.subscribe_condition_fulfilled(
                    agreement_id,
                    max(condition_def_dict['escrowReward'].timeout, self.EVENT_WAIT_TIMEOUT),
                    self._last_condition_fulfilled,
                    (agreement_id, cond_to_id),
                    from_block=block_number
                )
