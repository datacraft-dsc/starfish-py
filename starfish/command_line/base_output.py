"""

    Command line base output

"""

class BaseOutput():
    """
    Base output to handle the basic formating to Console, JSON and Test
    """

    def __init__(self):
        """init and clear the object"""
        self._header = {}
        self._items = {}
        self._rows = []

    def clear(self):
        """clear the collection of output items"""
        self._items = {}
        self._rows = []
        self._header = {}

    def show(self, text=None, name=None):
        if text is not None:
            if name is None:
                name = 'value'
            self.show_item(name, text)

    def show_item(self, name, value, format_text=None):
        self._items[name] = value

    def set_header(self, name, title, format_text=None):
        self._header[name] = {
            'name': name,
            'title': title,
            'format': format_text
        }
    def show_header(self):
        pass

    def set_item(self, name, value):
        self._items[name] = value

    def flush(self):
        self._rows.append(self._items)

    @property
    def rows(self):
        return self._rows

    @property
    def items(self):
        return self._items

    @property
    def header(self):
        return self._header
