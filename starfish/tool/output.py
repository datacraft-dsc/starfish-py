"""


    Starfish Tool Output

"""
import json
from typing import Any


class Output:
    def __init__(self) -> None:
        self._line_list = []
        self._values = {}
        self._error_list = []

    def add_error(self, line: str) -> None:
        self._error_list.append(line)

    def add_line(self, line: str) -> None:
        self._line_list.append(line)

    def set_value(self, key: str, value: str) -> None:
        self._values[key] = value

    def printout(self, is_json: bool) -> None:
        if self.has_errors:
            error_lines = '\nError: '. join(self.errors)
            print(f'Error: {error_lines}')
            return

        if is_json:
            if self.has_values:
                print(json.dumps(self.values, sort_keys=True, indent=2))
        else:
            if self.has_lines:
                print('\n'.join(self.lines))

    @property
    def errors(self) -> Any:
        return self._error_list

    @property
    def has_errors(self) -> bool:
        return len(self._error_list) > 0

    @property
    def lines(self) -> Any:
        return self._line_list

    @property
    def has_lines(self) -> bool:
        return len(self._line_list) > 0

    @property
    def values(self) -> Any:
        return self._values

    @property
    def has_values(self) -> bool:
        return len(self._values.keys()) > 0
