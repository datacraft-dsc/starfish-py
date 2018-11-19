import json
import os
import os.path
import logging
import sys
import traceback
import re

from ocean_plastic.command_line.console_output import ConsoleOutput
from ocean_plastic.command_line.json_output import JSONOutput
from ocean_plastic.exceptions import OceanCommandLineError
from squid_py.ocean.ocean import Ocean


HEX_STRING_FORMAT = '[0-fx]+'
INTEGER_FORMAT = '[0-9]+'
URL_STRING_FORMAT = '^http.*'

class CommandLine:
    def __init__(self, **kwargs):
        self._config_file = kwargs.get('config_file', None)
        self._output = kwargs.get('output', None)
        if self._output == None:
            if kwargs.get('is_json', False):
                self._output = JSONOutput()
            else:
                self._output = ConsoleOutput()
    def open(self):
        ocean = Ocean(config_file = self._config_file)
        return ocean

    def call(self, command, args):
        try:
            command_func = getattr(self, command.replace('-', '_'))
            command_func(args)
            return self._output
        except Exception as e:
            if isinstance(e, AttributeError):
                raise OceanCommandLineError('Cannot find command "{}"'.format(command))
            print(e)
            traceback.print_exc()
            raise OceanCommandLineError('Command failed "{}"'.format(command))

    def register(self, args):
        account_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT, INTEGER_FORMAT], 'You must provide an account id in argument #1')
        filename = self._assert_arg_filename(args, 1, 'You must provide a valid filename in argument #2')
        self._logger.debug('registering asset file %s', filename)
        name = None
        # optional name
        name = self._get_arg(args, 2, None)
        source_hash = Ocean.calculate_file_hash(filename)
        data_file = Ocean.get_meta_data_instance('data_file', source_hash = source_hash, name = name)
        meta_data = {
            'file' : data_file.as_meta_data()
        }
        self._output.clear()
        ocean = self.open()
        owner_account = self._get_account_from_value(ocean.get_accounts(), account_id)
        if not owner_account:
            raise OceanCommandLineError('You can only pass an index number or the actual account number to use')
        service = ocean.get_meta_storage_service(self._meta_storage_service)
        asset = ocean.register_asset(service, owner_account, meta_data)
        self._output.show_item('asset id', asset.get_id())
        self._output.show_item('owner', asset.get_owner())

    def upload(self, args):
        asset_id = self._assert_arg_match(args, 0,[HEX_STRING_FORMAT], 'You must provide an asset id in argument #1')
        price = int(self._assert_arg_match(args, 1, [INTEGER_FORMAT], 'You must provide a price in argument #2'))
        filename = self._assert_arg_filename(args, 2, 'You must provide a valid filename in argument #3')

        self._output.clear()
        ocean = self.open()
        asset = ocean.get_asset(asset_id)
        meta_data = asset.get_meta_data(self._meta_storage_service)
        data_file = Ocean.get_meta_data_instance(meta_data['file'])
        if data_file.get_source_hash() != Ocean.calculate_file_hash(filename):
            raise OceanError('The data file is not the same as registered with the asset')

        asset_data = None
        with open(filename , 'rb') as fp:
            asset_data = fp.read()
        asset.write_to_provider(self._asset_provider_service, price, asset_data)
        self._output.show_item('asset_id', asset.get_id())
        self._output.show_item('price', price)

    def credit(self, args):
        account_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT, INTEGER_FORMAT], 'You must provide an account id in argument #1')
        amount = int(self._assert_arg_match(args, 1, [INTEGER_FORMAT], 'You must provide an amount to credit in argument #2'))
        self._output.clear()
        ocean = self.open()

        owner_account = self._get_account_from_value(ocean.get_accounts(), account_id)
        if not owner_account:
            raise OceanCommandLineError('You can only pass an index number or the actual account number to use')

        receipt = owner_account.request_tokens(amount)
        credit_amount = owner_account.ocean
        self._output.show_item('owner', owner_account.address)
        self._output.show_item('balance', credit_amount)

    def buy(self, args):
        asset_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT], 'You must provide an asset id in argument #1')
        account_id = self._assert_arg_match(args, 1, [HEX_STRING_FORMAT, INTEGER_FORMAT], 'You must provide an account id in argument #2')
        self._output.clear()
        ocean = self.open()
        trader_account = ocean.get_account_from_value(account_id)
        if not trader_account:
            raise OceanCommandLineError('You can only pass an index number or the actual account number to use as a buyer account')

        service = ocean.get_asset_provider_service(self._asset_provider_service)
        trader = ocean.get_trader(trader_account)
        asset = ocean.get_asset(asset_id)
        asset_access = trader.buy(service, asset)
        if asset_access:
            self._output.show_item('access_id:', asset_access.get_access_id())
            self._output.show_item('secret token:', asset_access.get_token())
            self._output.show_item('from service id:', asset_access.get_asset_provider_service_id())


    def info(self, args):
        asset_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT], 'You must provide an asset id in argument #1')
        self._output.clear()
        ocean = self.open()
        asset = ocean.get_asset(asset_id)
        title_format = '{:40}'
        self._output.show_item('asset_id', asset.get_id(), '{:20}{:20}')
        self._output.show_item('owner:', asset.get_owner(), '{:20}{:20}')
        self._output.show_item('meta-data-service:',  asset.get_service_id(), '{:20}{:20}')
        meta_data_raw = asset.get_meta_data(self._meta_storage_service)
        self._output.show_item('meta-data:',  meta_data_raw, '{:20}{:80}')
        for name, meta_data_item in meta_data_raw.items():
            meta_data = ocean.get_meta_data_instance(meta_data_item)
            if meta_data.is_valid():
                self._output.show_item('meta_data_is_valid', 'True')
            else:
                self._output.show_item('meta_data_is_valid', 'False')

    def balance(self, args):
        self._output.clear()
        ocean = self.open()
        filter_account_id = None
        if len(args) > 0:
            account_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT, INTEGER_FORMAT], 'You must provide a valid account id')
            filter_account_id = ocean.get_account_from_value(account_id)
        index_format = '{:10}'
        account_format = '{:44}'
        balance_format = '{:>20}{:>40}'

        self._output.set_header('index', 'Index', '{:10}')
        self._output.set_header('account', 'Account', '{:44}')
        self._output.set_header('tokens', 'Ocean Tokens',  '{:>20}')
        self._output.set_header('ether', 'Ether', '{:>40}')
        self._output.show_header()
        index = 0
        for account_id, account in ocean.get_accounts().items():
            if filter_account_id == None or account_id == filter_account_id:
                self._output.set_item('index', str(index) )
                self._output.set_item('account', account_id )
                self._output.set_item('tokens', account.ocean_balance)
                self._output.set_item('ether', account.ether_balance)
                self._output.show_items()
            index = index + 1

    def list(self, args):
        self._output.clear()
        ocean = self.open()
        if len(args) > 0:
            if args[0] == 'access':
                service = ocean.get_asset_provider_service(self._asset_provider_service)
                rows  = service.get_access_logs()
                self._output.set_header('datetime', 'Datetime', '{:30}')
                self._output.set_header('access_id', 'Access Id', '{:68}')
                self._output.set_header('asset_id', 'Asset Id', '{:68}')
                self._output.show_header()
                for row in rows:
                    self._output.set_item('datetime', row['event_date_time'] )
                    self._output.set_item('access_id', row['access_id'] )
                    self._output.set_item('asset_id', row['asset_id'] )
                    self._output.show_items()

            elif args[0] == 'sale':
                service = ocean.get_asset_provider_service(self._asset_provider_service)
                asset_list = service.get_list()
                line_format = '{:80}{:42}{:>20}'

                self._output.set_header('asset_id', 'Asset Id', '{:68}')
                self._output.set_header('owner', 'Owner Account', '{:42}')
                self._output.set_header('price', 'Price', '{:>20}')
                self._output.show_header()

                for asset_id, row in asset_list.items():
                    self._output.set_item('asset_id', row['asset_id'] )
                    self._output.set_item('owner', row['owner'] )
                    self._output.set_item('price', row['price'] )
                    self._output.show_items()

            elif args[0] == 'sold':
                account_id = self._assert_arg_match(args, 1, [HEX_STRING_FORMAT, INTEGER_FORMAT], 'You must provide a valid account id in argument #3')
                owner_account = ocean.get_account_from_value(account_id)
                if owner_account == None:
                    raise OceanCommandLineError('You can only pass an index number or the actual account number to use')

                service = ocean.get_asset_provider_service(self._asset_provider_service)

                access_list = service.get_access_list(owner_account)
                self._output.set_header('access_id', 'Access Id', '{:68}')
                self._output.set_header('asset_id', 'Asset Id', '{:68}')
                self._output.set_header('owner', 'Owner Account', '{:42}')
                self._output.show_header()

                for access_id, row in access_list.items():
                    self._output.set_item('access_id', row['access_id'] )
                    self._output.set_item('asset_id', row['asset_id'] )
                    self._output.set_item('owner', row['consumer'] )
                    self._output.show_items()
            else:
                raise OceanCommandLineError('Error: unknown sub command "list {}"'.format(args[0]))
        else:
            service = ocean.get_meta_storage_service(self._meta_storage_service)
            asset_list = service.get_list()
            self._output.set_header('asset_id', 'Asset Id', '{:68}')
            self._output.set_header('meta_data', 'Meta Data', '{:140}')
            self._output.show_header()
            for asset_id, row in asset_list.items():
                self._output.set_item('asset_id', row['asset_id'])
                self._output.set_item('meta_data', row['meta_data'])
                self._output.show_items()

    # send these details to the market
    def setup(self, args):
        self._output.clear()
        ocean = self.open()
        self._output.show_item('Ethereum Node URL:', self._ethereum_url, '{:40}{:40}')
        self._output.show_item('Asset meta-storage service:', self._meta_storage_service, '{:40}{:40}')
        self._output.show_item('Asset provider service: ', self._asset_provider_service, '{:40}{:40}')


    def get(self, args):
        access_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT], 'You must provide an access id in argument #1')
        token = self._assert_arg_match(args, 1, [HEX_STRING_FORMAT], 'You must provide a token in argument #2')
        self._output.clear()
        ocean = self.open()
        service = ocean.get_asset_provider_service(self._asset_provider_service)
        self._output.show_item('data', service.get_access_item(access_id, token))


    def payments(self, args):
        self._output.clear()
        ocean = self.open()
        print(ocean.get_payment_list())

    def service(self, args):
        service_address =  self._assert_arg_match(args, 0, [HEX_STRING_FORMAT,URL_STRING_FORMAT], 'You must provide an asset id in argument #1')
        self._output.clear()
        ocean = self.open()
        service = ocean.get_service_from_address(service_address)
        self._output.set_header('service_id', 'Service Id', '{:68}')
        self._output.set_header('owner', 'Owner', '{:42}')
        self._output.set_header('service_type', 'Service Type', '{:42}')
        self._output.set_header('endpoint', 'Endpoint', '{:140}')
        self._output.show_header()

        self._output.set_item('service_id', service.get_id() )
        self._output.set_item('owner', service.get_owner() )
        self._output.set_item('service_type', service.get_service_type() )
        self._output.set_item('endpoint', service.get_endpoint() )
        self._output.show_items()

    def get_output(self):
        return self._output

    def _get_arg(self, args, index, default_value = None):
        if len(args) >= index + 1:
            return args[index]
        return default_value

    def _assert_arg_match(self, args, index, patterns, message):
        value = self._get_arg(args, index, None)
        if value:
            for pattern in patterns:
                if re.match(pattern, value):
                    return value
        raise OceanCommandLineError(message)

    def _assert_arg_filename(self, args, index, message):
        value = self._get_arg(args, index, None)
        if value and os.path.exists(value):
            return value
        raise OceanCommandLineError(message)

    def _get_account_from_value(self, accounts, value):
        result = None

        if re.match('^[0-9]$', value):
            result = accounts[list(accounts)[int(value)]]
        else:
            result = accounts[Web3.toHex(hexstr=value)]
        return result
