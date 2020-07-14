"""
DEX DID/DDO Python Library

.. moduleauthor: Bill


This version was copied from

https://github.com/oceanprotocol/squid-py/tree/4dc75b959f9f07101ff6ff30d33b4d95b9672834/squid_py/ddo


"""
from typing import Any

from .ddo import DDO                     # noqa: F401

from .public_key_base import (               # noqa: F401
    PUBLIC_KEY_STORE_TYPE_BASE64,
    PUBLIC_KEY_STORE_TYPE_BASE85,
    PUBLIC_KEY_STORE_TYPE_HEX,
    PUBLIC_KEY_STORE_TYPE_PEM
)


def create_ddo_object(ddo_data: Any) -> Any:
    ddo = None
    if isinstance(ddo_data, str):
        ddo = DDO(json_text=ddo_data)
    elif isinstance(ddo_data, dict):
        ddo = DDO(dictionary=ddo_data)
    elif isinstance(ddo_data, DDO):
        ddo = ddo_data
    return ddo
