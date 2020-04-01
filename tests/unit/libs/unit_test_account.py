import secrets

class UnitTestAccount():

    def __init__(self, password=None, key_value=None):
        self.test_address = '0x' + secrets.token_hex(20)
        self.test_password = secrets.token_hex(32)
        self.test_key_value = secrets.token_hex(32)
        if password:
            self.test_password = password
        if key_value:
            self.test_key_value = key_value

    @property
    def as_tuple(self):
        return (self.test_address, self.test_password, self.test_key_value)

    @property
    def as_dict(self):
        return {'address': self.test_address, 'password': self.test_password, 'key_value': self.test_key_value}

    @property
    def as_list(self):
        return [self.test_address, self.test_password, self.test_key_value]

    @property
    def address(self):
        return self.test_address
