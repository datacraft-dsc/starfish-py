"""
    Test utils.did

"""
import pytest
import secrets

from starfish.network.did import (
    did_validate,
    did_generate_random,
    did_to_id,
    id_to_did,
    is_did,
    did_parse,
    asset_did_validate,
    decode_to_asset_id,
    is_asset_did
)


def test_did_validate():
    test_did = did_generate_random()
    did_id = did_to_id(test_did)

    did_validate(test_did)
    did_validate(f'{test_did}/test')
    did_validate(f'{test_did}01021A2A/test')

    test_did = (did_id, did_id)
    with pytest.raises(TypeError):
        did_validate(test_did)

    assert(not is_did(test_did))

    test_did = 'test-text'
    with pytest.raises(ValueError, match='must start'):
        did_validate(test_did)
    assert(not is_did(test_did))

    test_did = 'did'
    with pytest.raises(ValueError, match='must start'):
        did_validate(test_did)
    assert(not is_did(test_did))

    test_did = f'did:extra-long:{did_id}'
    with pytest.raises(ValueError, match='"id" must have only'):
        did_validate(test_did)
    assert(not is_did(test_did))

    test_did = f'did:valid:0x01A2B3C'
    with pytest.raises(ValueError, match='path should only have hex characters'):
        did_validate(test_did)
    assert(not is_did(test_did))



def test_did_parse():
    test_did = did_generate_random()
    did_id = did_to_id(test_did)

    # basic parse
    value = did_parse(test_did)

    assert(value['method'] == 'dep')
    assert(f'0x{value["id"]}' == did_id)
    assert(value['id_hex'] == did_id)
    assert(value['fragment'] is None)
    assert(value['path'] is None)


    # test path
    test_path = secrets.token_hex(32)
    value = did_parse(f'{test_did}/{test_path}')

    assert(value['method'] == 'dep')
    assert(f'0x{value["id"]}' == did_id)
    assert(value['id_hex'] == did_id)
    assert(value['fragment'] == '')
    assert(value['path'] == test_path)


    # test fragment
    test_path = secrets.token_hex(32)
    test_fragment = secrets.token_urlsafe(32)
    value = did_parse(f'{test_did}/{test_path}#{test_fragment}')

    assert(value['method'] == 'dep')
    assert(f'0x{value["id"]}' == did_id)
    assert(value['id_hex'] == did_id)
    assert(value['fragment'] == test_fragment)
    assert(value['path'] == test_path)

def test_did_to_id():
    test_did = did_generate_random()
    did_id = did_to_id(test_did)
    value = did_parse(test_did)
    assert(value['id_hex'] == did_id)

def test_id_to_did():
    test_id = secrets.token_hex(32)
    did = id_to_did(test_id)
    value = did_parse(did)
    assert(value['id'] == test_id)

def test_decode_to_asset_id():
    asset_id = secrets.token_hex(32)
    test_did = did_generate_random()

    # decode did/asset_id
    did = f'{test_did}/{asset_id}'
    assert(asset_id == decode_to_asset_id(did))
    assert(is_asset_did(did))
    assert(asset_did_validate(did))

    # decode did/asset_id with leading 0x
    did = f'{test_did}/0x{asset_id}'
    assert(asset_id == decode_to_asset_id(did))
    assert(is_asset_did(did))
    assert(asset_did_validate(did))

    # decode asset_id
    assert(asset_id == decode_to_asset_id(asset_id))

    # decode asset_id with leading 0x
    assert(asset_id == decode_to_asset_id(f'0x{asset_id}'))

    # fail decode with only did
    with pytest.raises(ValueError, match='Unable to get an asset_id'):
        assert(decode_to_asset_id(test_did))

    with pytest.raises(ValueError, match='does not have an asset_id'):
        assert(asset_did_validate(test_did))

    assert(not is_asset_did(test_did))

    # fail decode with invalid asset_id length is too long
    did = f'{test_did}/{asset_id}12A3B4C'
    with pytest.raises(ValueError, match='asset_id is not valid '):
        assert(decode_to_asset_id(did))

    with pytest.raises(ValueError, match='has an invalid asset_id'):
        assert(asset_did_validate(did))

    # passes did valdiaton but fails asset_did validation
    did = f'{test_did}/00112233445566778899AA'
    assert(decode_to_asset_id(did))

    with pytest.raises(ValueError, match='has an invalid asset_id'):
        assert(asset_did_validate(did))

    assert(not is_asset_did(did))

