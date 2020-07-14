"""
DID utils

"""

import re
import secrets
import warnings
from typing import Any

from urllib.parse import urlparse
from eth_utils import remove_0x_prefix

from web3 import Web3

from starfish.ddo import create_ddo_object
from starfish.types import DIDParts

NETWORK_DID_METHOD = 'dep'


def did_validate(did: str) -> bool:
    """

    Validate a did string.

    :param str did: DID string to validate, this can be an agent did or an asset_did
    :return: True if the did is valid
    :raise: TypeError if did is not a string
    :raise: ValueError if the DID is invalid

    """
    if not isinstance(did, str):
        raise TypeError('Expecting DID of string type, got %s of %s type' % (did, type(did)))

    if not re.match('^did:', did, re.IGNORECASE):
        raise ValueError(f'DID {did} must start with the text "did"')

    if not re.match('^did:([a-z0-9]+):', did, re.IGNORECASE):
        raise ValueError(f'DID {did} "id" must have only a-z 0-9 characters')

    if not re.match('^did:[a-z0-9]+:[a-f0-9]{64}.*', did, re.IGNORECASE):
        raise ValueError(f'DID {did} path should only have hex characters')
    return True


def is_did(did: str) -> bool:
    """

    Return True or False if the DID is valid.

    :param str did: DID string to validate, this can be an agent did or an asset_did

    """
    try:
        return did_validate(did)
    except (ValueError, TypeError):
        pass
    return False


def asset_did_validate(asse_did: str) -> bool:
    """

    Validates a asset_did in the format 'did:dep:<64_hex_chars>/<64_hex_chars>'

    :param str asse_did: Asset did to validate
    :return: True if validation is correct
    :raises: TypeError if did is not a string
    :raises: ValueError if the DID or the asset_id part of the DID is not valid

    """
    value = did_parse(asse_did)
    if value['path'] is None:
        raise ValueError(f'DID {asse_did} does not have an asset_id')
    if not re.match(r'^[0x]{0,2}[a-f0-9]{64}$', value['path']):
        raise ValueError(f'DID {asse_did} has an invalid asset_id')
    return True


def is_asset_did(asse_did: str) -> bool:
    """

    Return True or False if the asset_did is valid

    """
    try:
        return asset_did_validate(asse_did)
    except (ValueError, TypeError):
        pass
    return False


def did_parse(did: str) -> DIDParts:
    """

    parse a DID into it's parts.

    did:<method>:<id/id_hex>[/<path>[#<fragment>]]

    :param str did: DID to parse into seperate components
    :return: Dict of parts they are:
        method,
        id,
        id_hex,
        path,
        fragment


    """

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


def did_generate_random() -> str:
    """

    Return a randomly generated DID

    """
    did_id = secrets.token_hex(32)
    return id_to_did(did_id)


def did_to_id(did: str) -> str:
    """

    Convert a DID to an hex id value

    """

    data = did_parse(did)
    return data['id_hex']


def id_to_did(did_id: str) -> str:
    """

    Convert an hex id to a DID

    """
    did_id = remove_0x_prefix(did_id)
    return f'did:{NETWORK_DID_METHOD}:{did_id}'


def decode_to_asset_id(asset_did_id: str) -> str:
    """

    Try to decode an id to an asset_id. The id can be a full asset_did, asset_id ( 32 hex number)

    :param str asset_did_id: string to try to decode
    :return: asset_id as a hex string, with no leading '0x'
    :raises ValueError: if no path exists in the asset_did or the path is invalid


    """

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


def did_to_asset_id(did: str) -> str:
    """

    Depretaated function, use `decode_to_asset_id` instead
    """
    warnings.warn('use "decode_to_asset_id" instead', DeprecationWarning)
    return decode_to_asset_id(did)


def get_did_from_ddo(ddo_data: Any) -> str:
    ddo = create_ddo_object(ddo_data)
    if ddo:
        return ddo.did
    return None
