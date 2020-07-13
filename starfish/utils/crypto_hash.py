"""

CryptoHash utils

"""
from typing import Any

from Crypto.Hash import SHA3_256
from web3 import Web3


def hash_sha3_256(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')

    messageDigest = SHA3_256.new()
    messageDigest.update(data)
    return messageDigest.hexdigest()


def hash_keccak_256(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')

    return Web3.toHex(Web3.sha3(data))[2:]
