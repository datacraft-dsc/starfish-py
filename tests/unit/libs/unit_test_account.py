import secrets

class UnitTestAccount():

    def __init__(self):
        self.test_address = '0x' + secrets.token_hex(20)
        self.test_password = secrets.token_hex(32)
        self.test_ether = secrets.randbelow(10000000)
        self.test_tokens = secrets.randbelow(10000000)

    @property
    def as_tuple(self):
        return (self.test_address, self.test_password)
        
    @property
    def as_dict(self):
        return {'address': self.test_address, 'password': self.test_password}

    @property
    def as_list(self):
        return [self.test_address, self.test_password]