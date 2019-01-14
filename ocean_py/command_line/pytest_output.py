"""

    Command line Test output

"""


from .base_output import (
    BaseOutput,
)

class PyTestOutput(BaseOutput):

    def __init__(self):
        BaseOutput.__init__(self)

    def show(self, text=None, name=None):
        if text:
            if name is None:
                name = 'value'
            self.show_item(name, text)

    def show_item(self, name, value, format_text=None):
        self._items[name] = value

    def show_header(self):
        pass

    def show_items(self):
        self._rows.append(self._items)
        self._items = {}

    def flush(self):
        pass
