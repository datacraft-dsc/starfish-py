"""
DID utils

"""

import secrets
import re
from urllib.parse import urlparse
from web3 import Web3

OCEAN_DID_METHOD = 'dep'

def did_parse(did):
    """parse a DID into it's parts"""
    if not isinstance(did, str):
        raise TypeError('Expecting DID of string type, got %s of %s type' % (did, type(did)))

    match = re.match('^did:([a-z0-9]+):([a-zA-Z0-9-.]+)(.*)', did)
    if not match:
        raise ValueError('DID %s does not seem to be valid.' % did)

    result = {
        'method': match.group(1),
        'id': match.group(2),
        'path': None,
        'fragment': None,
        'id_hex': None
    }

    uri_text = match.group(3)
    if uri_text:
        uri = urlparse(uri_text)
        result['fragment'] = uri.fragment
        if uri.path:
            result['path'] = uri.path[1:]

    if result['method'] == OCEAN_DID_METHOD and re.match('^[0-9A-Fa-f]{1,64}$', result['id']):
        result['id_hex'] = Web3.toHex(hexstr=result['id'])

    if not result['id_hex'] and result['id'].startswith('0x'):
        result['id_hex'] = result['id']

    return result

def did_generate_random():
    did_id = secrets.token_hex(32)
    return f'did:{OCEAN_DID_METHOD}:{did_id}'


def did_to_asset_id(did):
    data = did_parse(did)
    asset_id = None
    if data['id_hex']:
        asset_id = data['id_hex']
    if data['path'] and re.match('^[0-9A-Fa-f]{1,64}$', data['path']):
        asset_id = '0x' + data['path']
    return asset_id
