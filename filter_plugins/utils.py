import os

import bcrypt

def bcrypt_password(value):
    return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())

def valid(value):
    return not ('"' in value or "'" in value)

class FilterModule(object):

    filter_map =  {
        'bcrypt': bcrypt_password,
        'valid': valid
    }

    def filters(self):
        return self.filter_map
