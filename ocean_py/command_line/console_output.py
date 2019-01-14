"""

    Command line console outptu

"""

import json

from .base_output import BaseOutput

class ConsoleOutput(BaseOutput):

    def show(self, text=None, name=None):
        if text:
            print(text)

    def show_item(self, name, value, format_text=None):
        if format_text is None:
            format_text = '{:20}{:80}'
        if isinstance(value, dict):
            value = json.dumps(value)
        print(format_text.format(name, value))

    def show_header(self):
        line = []

        for header in self._header.values():
            line.append(header['format'].format(header['title']))

        if line:
            print("".join(line))

    def show_items(self):
        line = []
        for name, header in self._header.items():
            value = ''
            if name in self._items:
                value = self._items[name]
            line.append(header['format'].format(value))
        if line:
            print("".join(line))

    def flush(self):
        pass
