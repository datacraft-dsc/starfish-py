"""

    ConvexRegistry

"""
import logging

from convex_api.exceptions import ConvexAPIError
from convex_api.utils import to_address


logger = logging.getLogger(__name__)

QUERY_ACCOUNT_ADDRESS = 9


class ConvexRegistry:

    def __init__(self, convex):
        self._convex = convex
        self._address = None
        self._items = {}

    def is_registered(self, name):
        return self.item(name) is not None

    def item(self, name):
        if name not in self._items:
            result = self._convex.query(f'(get cns-database (symbol "{name}"))', self.address)
            logger.debug(f'cns-database: {result}')
            self._items[name] = None
            if result and 'value' in result and isinstance(result['value'], (list, tuple)):
                self._items[name] = result['value']
        return self._items[name]

    def clear(self):
        self._items = {}
        self._address = None

    def register(self, name, contract_address, account):
        result = self._convex.send(f'(call {self.address} (register {{:name "{name}"}}))', account)
        logger.debug(f'register result: {result}')
        if result and 'value' in result:
            try:
                result = self._convex.send(f'(call {self.address} (cns-update "{name}" {contract_address}))', account)
                logger.debug(f'cns-update result: {result}')
                if result and 'value' in result:
                    items = result['value']
                    if name in items:
                        item = items[name]
                        self._items[name] = item
                        return item
            except ConvexAPIError as e:
                logger.debug(f'convex error: {e}')

    def resolve_owner(self, name):
        item = self.item(name)
        if item:
            return item[1]

    def resolve_address(self, name):
        item = self.item(name)
        if item:
            return item[0]

    @property
    def address(self):
        if self._address is None:
            result = self._convex.query('(address *registry*)', QUERY_ACCOUNT_ADDRESS)
            self._registry_address = to_address(result['value'])
            logger.debug(f'registry_address: {self._registry_address}')
        return self._registry_address
