#!/usr/bin/env python3
"""

    Wait for the local network node to be build and startup

    This script waits for all of the contracts to be found and downloaded


"""

import argparse
import logging

from starfish import DNetwork

DEFAULT_NETWORK_URL = 'http://localhost:8545'
DEFAULT_TIMEOUT = 480


def main():

    parser = argparse.ArgumentParser(description='Wait for local test network')

    parser.add_argument(
        '-u',
        '--url',
        default=DEFAULT_NETWORK_URL,
        help=f'URL of the local network node. Default: {DEFAULT_NETWORK_URL}',
    )

    parser.add_argument(
        '-t',
        '--timeout',
        default=DEFAULT_TIMEOUT,
        help=f'Seconds to wait for the network to startup. Default: {DEFAULT_TIMEOUT}',
    )

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help=f'Debug mode on or off. Default: False',
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    print('wating for network startup...')
    network = DNetwork(args.url)
    if network.load_development_contracts(args.timeout):
        print(f'Network at {args.url} is ready')
    else:
        print(f'Timeout: Network at {args.url} is not ready')


if __name__ == "__main__":
    main()
