"""
DID utils

"""

import re
import secrets
import warnings

from urllib.parse import urlparse
from eth_utils import remove_0x_prefix

from web3 import Web3


NETWORK_DID_METHOD = 'dep'


def did_validate(did):
    if not isinstance(did, str):
        raise TypeError('Expecting DID of string type, got %s of %s type' % (did, type(did)))

    if not re.match('^did:', did, re.IGNORECASE):
        raise ValueError('DID must start with the text "did"')

    if not re.match('^did:([a-z0-9]+):', did, re.IGNORECASE):
        raise ValueError('DID "id" must have only a-z 0-9 characters')

    if not re.match('^did:[a-z0-9]+:[a-f0-9]{64}.*', did, re.IGNORECASE):
        raise ValueError(f'DID path should only have hex characters.')
    return True


def is_did(did):
    try:
        return did_validate(did)
    except (ValueError, TypeError):
        pass
    return False


def is_asset_did(did):
    try:
        value = did_parse(did)
        if value['path'] is None:
            raise ValueError(f'DID {did} is not a valid asset_did')
        if not re.match(r'^[0x]{0,2}[a-f0-9]{64}$', value['path']):
            raise ValueError(f'DID {did} as an invalid asset_id')
        return True
    except (ValueError, TypeError):
        pass
    return False


def did_parse(did):
    """parse a DID into it's parts"""

    did_validate(did)

    match = re.match('^did:([a-z0-9]+):([a-f0-9]{64})(.*)', did, re.IGNORECASE)
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

    if result['method'] == NETWORK_DID_METHOD and re.match('^[0-9a-f]{1,64}$', result['id'], re.IGNORECASE):
        result['id_hex'] = Web3.toHex(hexstr=result['id'])

    if not result['id_hex'] and result['id'].startswith('0x'):
        result['id_hex'] = result['id']

    return result


def did_generate_random():
    did_id = secrets.token_hex(32)
    return id_to_did(did_id)


def did_to_id(did):
    data = did_parse(did)
    return data['id_hex']


def id_to_did(did_id):
    did_id = remove_0x_prefix(did_id)
    return f'did:{NETWORK_DID_METHOD}:{did_id}'


def decode_to_asset_id(asset_did_id):
    asset_id = None
    if re.match(r'^[0-9a-fx]+$', asset_did_id, re.IGNORECASE):
        asset_id = Web3.toHex(hexstr=asset_did_id)
    else:
        data = did_parse(asset_did_id)
        if data['path'] is None:
            raise ValueError(f'Unable to get an asset_id from an agent DID address {asset_did_id}')

        if data['path'] and re.match('^[0-9a-fx]{1,66}$', data['path'], re.IGNORECASE):
            asset_id = data['path']
        else:
            raise ValueError(f'DID with asset_id is not valid {asset_did_id}')
    return remove_0x_prefix(asset_id)


def did_to_asset_id(did):
    warnings.warn('use "decode_to_asset_id" instead', DeprecationWarning)
    return decode_to_asset_id(did)
