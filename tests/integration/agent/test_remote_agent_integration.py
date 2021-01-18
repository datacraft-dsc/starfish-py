"""

    Test RemoteAgent Integration


"""
import secrets

from starfish.agent.remote_agent import RemoteAgent


def _test_remote_agent_collecton_add_get(remote_agent_invokable):

    asset_list_length = 10

    assert(remote_agent_invokable.is_service('collection'))

    name = secrets.token_hex(32)
    add_asset_list = []
    for index in range(0, asset_list_length):
        asset_id = f'0x{secrets.token_hex(32)}'
        add_asset_list.append(asset_id)

    result = remote_agent_invokable.add_collection_items(name, add_asset_list)
    assert(result)
    assert(result == add_asset_list)

    result = remote_agent_invokable.add_collection_items(name, add_asset_list)
    assert(result == [])


    result = remote_agent_invokable.get_collection_items()
    assert(result)
    assert(name in result)
    assert(result[name] == add_asset_list)

    remove_asset_list = []
    for index in range(0, int(asset_list_length / 2)):
        remove_asset_list.append(add_asset_list.pop())

    result = remote_agent_invokable.remove_collection_items(name, remove_asset_list)
    assert(result)
    assert(result == remove_asset_list)


    result = remote_agent_invokable.get_collection_items()
    assert(result)

def _test_remote_agent_not_supported_collecton(remote_agent_surfer):

    assert(remote_agent_surfer.is_service('collection') == False)
