import secrets

class UnitTestAccount():

    def __init__(self, password = None):
        self.test_address = '0x' + secrets.token_hex(20)
        if password:
            self.test_password = password
        else:
            self.test_password = secrets.token_hex(32)
        self.test_ether = 1 + secrets.randbelow(100)
        self.test_tokens = 5 + secrets.randbelow(100)

    @property
    def as_tuple(self):
        return (self.test_address, self.test_password)

    @property
    def as_dict(self):
        return {'address': self.test_address, 'password': self.test_password}

    @property
    def as_list(self):
        return [self.test_address, self.test_password]

    @property
    def address(self):
        return self.test_address
