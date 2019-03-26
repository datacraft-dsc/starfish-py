#!/usr/bin/env python
"""

    Tests for `ocean agent command line`.

"""
import unittest
import random
import os
import logging

from pytest import (
    mark,
    raises,
)

from starfish.command_line import CommandLine
from starfish.command_line.pytest_output import PyTestOutput


def test_command_line_balance():

    test_output = PyTestOutput()
    command_line = CommandLine(output = test_output)
    args = []
    output = command_line.call('balance', args)
    index = 0
    for row in output.rows:
        assert int(row['index']) == index
        assert row['account'] == command_line._ocean.accounts[row['account']].address
        assert 'tokens' in row
        assert 'ether' in row
        index += 1

"""
def test_command_line_asset():

    logging.basicConfig(level = logging.DEBUG)
    logger = logging.getLogger(os.path.basename(__file__))

    command_line = CommandLine(ethereum_url = ETHEREUM_URL,
        keeper_contracts_path = KEEPER_CONTRACT_FILES,
        meta_storage_service = META_STORAGE_URL,
        asset_provider_service = ASSET_PROVIDER_URL,
        logger = logger,
        output = PyTestOutput()
    )
    ocean = command_line.open()

    # register an asset
    test_name = 'Name for asset ' + ASSET_FILE
    args = [str(ASSET_OWNER_ACCOUNT_INDEX), ASSET_FILE, test_name]
    output = command_line.call('register', args)
    result = output.get_items()
    assert result != None
    assert result['owner'] == ocean.accounts[ASSET_OWNER_ACCOUNT_INDEX]
    asset_id = result['asset id']

    # get asset info
    args = [asset_id]
    output = command_line.call('info', args)
    result = output.get_items()
    assert result != None
    assert result['owner:'] == ocean.accounts[ASSET_OWNER_ACCOUNT_INDEX]
    assert result['asset_id'] == asset_id

    # get asset list
    args = []
    output = command_line.call('list', args)
    result = output.get_rows()
    assert result != None
    is_found = False
    for row in result:
        if row['asset_id'] == asset_id:
            is_found = True
            break
    assert is_found == True

    # upload an asset
    args = [asset_id, str(ASSET_PRICE), ASSET_FILE]
    output = command_line.call('upload', args)
    result = output.get_items()
    assert result != None
    assert result['asset_id'] == asset_id
    assert result['price'] == ASSET_PRICE

    # asset list for sale

    args = ['sale']
    output = command_line.call('list', args)
    result = output.get_rows()
    assert result != None
    is_found = False
    for row in result:
        if row['asset_id'] == asset_id:
            is_found = True
            break
    assert is_found == True

    # credit test account with tokens
    args = [str(ASSET_BUYER_ACCOUNT_INDEX), str(ASSET_PRICE)]
    output = command_line.call('credit', args)
    result = output.get_items()
    assert result != None
    assert result['credit_amount'] == ASSET_PRICE
    assert result['owner'] == ocean.accounts[ASSET_BUYER_ACCOUNT_INDEX]

    # buy an asset
    args = [asset_id, str(ASSET_BUYER_ACCOUNT_INDEX)]
    output = command_line.call('buy', args)
    result = output.get_items()
    assert result != None
    assert result['access_id:'] != None
    assert result['secret token:'] != None
    assert result['from service id:'] != None

    access_id = result['access_id:']
    token = result['secret token:']


    # get asset list as sold
    args = ['sold', str(ASSET_BUYER_ACCOUNT_INDEX)]
    output = command_line.call('list', args)
    result = output.get_rows()
    assert result != None
    is_found = False
    for row in result:
        if row['access_id'] == access_id and row['asset_id'] == asset_id:
            is_found = True
    assert is_found == True

    #get asset data
    args = [access_id, token]
    output = command_line.call('get', args)
    result = output.get_items()
    assert result != None
    assert 'data' in result
    assert result['data'] != None
"""
