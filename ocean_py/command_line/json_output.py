"""

    Command line JSON output

"""
import json

from .base_output import BaseOutput

class JSONOutput(BaseOutput):


    def show(self, text=None, name=None):
        if self._rows:
            print(json.dumps(self._rows))

    def show_item(self, name, value, format_text=None):
        item = {name: value}
        print(json.dumps(item))

    def show_header(self):
        pass

    def set_item(self, name, value):
        self._items[name] = value

    def show_items(self):
        self._rows.append(self._items)
        self._items = {}

    def flush(self):
        if self._rows:
            print(json.dumps(self._rows))
        if self._items:
            print(json.dumps(self._items))
        self._rows = []
        self._items = {}
