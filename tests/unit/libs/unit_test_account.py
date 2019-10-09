import secrets

class UnitTestAccount():

    def __init__(self, password=None, keyfile=None):
        self.test_address = '0x' + secrets.token_hex(20)
        self.test_password = secrets.token_hex(32)
        self.test_keyfile = secrets.token_hex(32)
        if password:
            self.test_password = password
        if keyfile:
            self.test_keyfile = keyfile
        self.test_ether = 1 + secrets.randbelow(100)
        self.test_tokens = 5 + secrets.randbelow(100)
        self._agent_adapter = None

    @property
    def as_tuple(self):
        return (self.test_address, self.test_password, self.test_keyfile)

    @property
    def as_dict(self):
        return {'address': self.test_address, 'password': self.test_password, 'keyfile': self.test_keyfile}

    @property
    def as_list(self):
        return [self.test_address, self.test_password, self.test_keyfile]

    @property
    def address(self):
        return self.test_address

    @property
    def agent_adapter(self):
        return self._agent_adapter

    @agent_adapter.setter
    def agent_adapter(self, agent_adapter):
        self._agent_adapter = agent_adapter

