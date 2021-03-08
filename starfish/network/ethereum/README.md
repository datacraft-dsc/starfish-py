## Ethereum Notes

**Network.Ethereum has been disabled..**


Currently the local test geth ethereum network is not working.

We are getting the following error ( see below). Since this error is from an old security fix to stop 3rd party access to a ethereum
RPC connection, this could be a web3 library bug or the new geth app is not supporting the correct protocol.

## Error Log


```
====================================================================================================== FAILURES =======================================================================================================
________________________________________________________________________________________________ test_network_account _________________________________________________________________________________________________

ethereum_network = <starfish.network.ethereum.ethereum_network.EthereumNetwork object at 0x7f3582777130>
ethereum_accounts = [<starfish.network.ethereum.ethereum_account.EthereumAccount object at 0x7f35826e3f10>, <starfish.network.ethereum.ethereum_account.EthereumAccount object at 0x7f35826e3820>]

    def test_network_account(ethereum_network, ethereum_accounts):
        test_account = ethereum_accounts[0]
        ether_balance = ethereum_network.get_ether_balance(test_account)
        assert(ether_balance)

>       ethereum_network.request_test_tokens(test_account, TEST_AMOUNT)

tests/integration/network/ethereum/test_ethereum_network.py:27:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
starfish/network/ethereum/ethereum_network.py:133: in request_test_tokens
    tx_hash = dispenser_contract.request_tokens(account, amount)
starfish/network/ethereum/contract/dispenser_contract.py:22: in request_tokens
    return self.call('requestTokens', amount, account)
starfish/network/ethereum/contract/contract_base.py:53: in call
    result = self._call_as_transaction(contract_function_call, account, transact)
starfish/network/ethereum/contract/contract_base.py:103: in _call_as_transaction
    tx_hash = self._web3.eth.send_raw_transaction(signed.rawTransaction)
venv/lib/python3.9/site-packages/web3/module.py:58: in caller
    result = w3.manager.request_blocking(method_str, params, error_formatters)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <web3.manager.RequestManager object at 0x7f35827770d0>, method = 'eth_sendRawTransaction'
params = ('0xf88621824e208301c2299409e0fa804e68a6e3f2df4393f30a871ead432c3b80a4eef9c27c0000000000000000000000000000000000000000...28fc7a81f3dc7aa96b98022279cc39ed25bcd5d9a27b423181a073f58ea3ec37519d17b5bd79ffdbe4c96130c1e99bced92e916e35cc879c5b21',)
error_formatters = <cyfunction identity at 0x7f35877f8930>

    def request_blocking(
        self,
        method: Union[RPCEndpoint, Callable[..., RPCEndpoint]],
        params: Any,
        error_formatters: Optional[Callable[..., Any]] = None,
    ) -> Any:
        """
        Make a synchronous request using the provider
        """
        response = self._make_request(method, params)

        if "error" in response:
            apply_error_formatters(error_formatters, response)
>           raise ValueError(response["error"])
E           ValueError: {'code': -32000, 'message': 'only replay-protected (EIP-155) transactions allowed over RPC'}

venv/lib/python3.9/site-packages/web3/manager.py:158: ValueError
```
