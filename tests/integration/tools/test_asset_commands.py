"""

    Test Intergation for Assets

"""

import hashlib
import os
import secrets
import tempfile
from eth_utils import remove_0x_prefix


from unittest.mock import Mock

from starfish.utils.did import did_to_id
from starfish.agent import AgentManager

from starfish.tool.command.asset_store_command import AssetStoreCommand
from starfish.tool.command.asset_download_command import AssetDownloadCommand
from starfish.tool.output import Output

def create_random_filename():
    random_name = secrets.token_hex(12)
    return os.path.join(tempfile.gettempdir(), f'test_{random_name}.dat')

def create_test_file(filename):
    with open(filename, 'wb') as fp:
        for index in range(0, 100):
            fp.write(secrets.token_bytes(2048))

def hash_file(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as fp:
        md5.update(fp.read())
    return md5.hexdigest()

def test_asset_store_and_download_command(config, network, remote_agent, accounts):
    args = Mock()

    test_upload_filename = create_random_filename()
    create_test_file(test_upload_filename)

    args.url = config.network_url
    remote_agent = config.agent_list['remote']
    args.username = remote_agent['username']
    args.password = remote_agent['password']
    args.agent = remote_agent['url']
    args.name = 'Test Asset Store'
    args.filename = test_upload_filename
    asset_store = AssetStoreCommand()
    output = Output()
    asset_store.execute(args, output)
    assert(output.values['asset_did'])
    upload_asset_did = output.values['asset_did']

    # register agent in network using it's did

    result = AgentManager.resolve_agent(args.agent, network, args.username, args.password)
    register_account = accounts[0]
    did_id = remove_0x_prefix(did_to_id(upload_asset_did))
    network.register_did(register_account, f'did:dep:{did_id}', result['ddo_text'])


    args = Mock()
    test_download_filename = create_random_filename()
    args.url = config.network_url
    remote_agent = config.agent_list['remote']
    args.username = remote_agent['username']
    args.password = remote_agent['password']
    args.asset_did = upload_asset_did
    args.filename = test_download_filename
    asset_download = AssetDownloadCommand()
    output = Output()
    asset_download.execute(args, output)

    assert(output.values['asset_did'])
    assert(os.path.exists(test_download_filename))

    if os.path.exists(test_download_filename):
        os.unlink(test_download_filename)
    os.unlink(test_upload_filename)
