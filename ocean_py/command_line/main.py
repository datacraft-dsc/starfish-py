import os
import os.path
import traceback
import re
from ocean_py.command_line.console_output import ConsoleOutput
from ocean_py.command_line.json_output import JSONOutput
from ocean_py.exceptions import OceanCommandLineError
from squid_py.ocean.ocean import Ocean


HEX_STRING_FORMAT = '[0-fx]+'
INTEGER_FORMAT = '[0-9]+'
URL_STRING_FORMAT = '^http.*'

class CommandLine:
    def __init__(self, **kwargs):
        self._config_file = kwargs.get('config_file', None)
        self._output = kwargs.get('output', None)
        if self._output is None:
            if kwargs.get('is_json', False):
                self._output = JSONOutput()
            else:
                self._output = ConsoleOutput()
    def open(self):
        ocean = Ocean(config_file=self._config_file)
        return ocean

    def call(self, command, args):
        try:
            command_func = getattr(self, command.replace('-', '_'))
            command_func(args)
            return self._output
        except Exception as exception:
            if isinstance(exception, AttributeError):
                raise OceanCommandLineError('Cannot find command "{}"'.format(command))
            print(exception)
            traceback.print_exc()
            raise OceanCommandLineError('Command failed "{}"'.format(command))

    def balance(self, args):
        self._output.clear()
        ocean = self.open()
        filter_account_id = None
        if args:
            account_id = self._assert_arg_match(args, 0, [HEX_STRING_FORMAT, INTEGER_FORMAT], 'You must provide a valid account id')
            filter_account_id = ocean.get_account_from_value(account_id)
        # index_format = '{:10}'
        # account_format = '{:44}'
        # balance_format = '{:>20}{:>40}'

        self._output.set_header('index', 'Index', '{:10}')
        self._output.set_header('account', 'Account', '{:44}')
        self._output.set_header('tokens', 'Ocean Tokens', '{:>20}')
        self._output.set_header('ether', 'Ether', '{:>40}')
        self._output.show_header()
        index = 0
        for account_id, account in ocean.get_accounts().items():
            if filter_account_id or account_id == filter_account_id:
                self._output.set_item('index', str(index))
                self._output.set_item('account', account_id)
                self._output.set_item('tokens', account.ocean_balance)
                self._output.set_item('ether', account.ether_balance)
                self._output.show_items()
            index = index + 1

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

    @staticmethod
    def _get_account_from_value(accounts, value):
        result = None

        if re.match('^[0-9]$', value):
            result = accounts[list(accounts)[int(value)]]
        else:
            result = accounts[Web3.toHex(hexstr=value)]
        return result
