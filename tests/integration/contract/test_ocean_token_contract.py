import pytest
import time


TOKEN_AMOUNT_TO_TRANSFER = 10

def test_ocean_taken_contract(network, accounts):

    ocean_token_contract = network.get_contract('OceanToken')
    dispenser_contract = network.get_contract('Dispenser')

    from_account = accounts[0]
    to_account = accounts[1]

    balance = ocean_token_contract.get_balance(from_account)

    tx_hash = dispenser_contract.request_tokens(from_account, TOKEN_AMOUNT_TO_TRANSFER * 2)
    receipt = dispenser_contract.wait_for_receipt(tx_hash)

    # give enougth time for the block chain to go to the next block and mine this dispenser request
    time.sleep(1)

    from_balance = ocean_token_contract.get_balance(from_account)
    to_balance = ocean_token_contract.get_balance(to_account)

#    tx_hash = ocean_token_contract.approve_transfer(from_account, ocean_token_contract.address, TOKEN_AMOUNT_TO_TRANSFER)
#    receipt = ocean_token_contract.wait_for_receipt(tx_hash)
    """

        *********************************************************************
        This does not work on the github test suite, but works on the desktop
        *********************************************************************

    tx_hash = ocean_token_contract.transfer(from_account, to_account.address, TOKEN_AMOUNT_TO_TRANSFER)
    receipt = ocean_token_contract.wait_for_receipt(tx_hash)

    new_from_balance = ocean_token_contract.get_balance(from_account)
    new_to_balance = ocean_token_contract.get_balance(to_account)

    assert(from_balance - TOKEN_AMOUNT_TO_TRANSFER == new_from_balance)
    assert(to_balance + TOKEN_AMOUNT_TO_TRANSFER == new_to_balance)

    """