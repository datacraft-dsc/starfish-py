import os
import os.path
import traceback
import re
from starfish.command_line.console_output import ConsoleOutput
from starfish.command_line.json_output import JSONOutput
from starfish.exceptions import OceanCommandLineError
from starfish import Ocean


HEX_STRING_FORMAT = '[0-fx]+'
INTEGER_FORMAT = '[0-9]+'
URL_STRING_FORMAT = '^http.*'


def get_default(args, index, default=None):
    if len(args) > index:
        return args[index]
    return default

def assert_arg_match(args, index, patterns, message):
    value = get_default(args, index)
    if value:
        for pattern in patterns:
            if re.match(pattern, value):
                return value
    raise OceanCommandLineError(message)

def assert_arg_filename(args, index, message):
    value = get_default(args, index)
    if value and os.path.exists(value):
        return value
    raise OceanCommandLineError(message)


class CommandLine:
    def __init__(self, **kwargs):
        self._ocean = Ocean(**kwargs)
        self._output = kwargs.get('output', None)
        if self._output is None:
            if kwargs.get('is_json', False):
                self._output = JSONOutput()
            else:
                self._output = ConsoleOutput()

    def call(self, command, args):
        try:
            command_func = getattr(self, command.replace('-', '_'))
            command_func(args)
            return self._output
        except Exception as exception:
            if isinstance(exception, AttributeError):
                raise OceanCommandLineError(f'Cannot find command "{command}"')
            print(exception)
            traceback.print_exc()
            raise OceanCommandLineError(f'Command failed "{command}"')

    def balance(self, args):
        self._output.clear()
        filter_account_id = None
        if args:
            filter_account_id = assert_arg_match(args, 0,
                                                 [HEX_STRING_FORMAT,
                                                  INTEGER_FORMAT],
                                                 'You must provide a valid account id')
        self._output.set_header('index', 'Index', '{:10}')
        self._output.set_header('account', 'Account', '{:44}')
        self._output.set_header('tokens', 'Ocean Tokens', '{:>20}')
        self._output.set_header('ether', 'Ether', '{:>40}')
        self._output.show_header()
        index = 0
        for account_id, account in self._ocean.accounts.items():
            if not filter_account_id or account_id == filter_account_id:
                self._output.set_item('index', str(index))
                self._output.set_item('account', account_id)
                self._output.set_item('tokens', account.ocean_balance)
                self._output.set_item('ether', account.ether_balance)
                self._output.show_items()
            index = index + 1
