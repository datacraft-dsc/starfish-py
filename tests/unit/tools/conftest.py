import argparse
import pytest



@pytest.fixture(scope='module')
def parser():
    parser = argparse.ArgumentParser(description='Starfish Tools')
    return parser


@pytest.fixture(scope='module')
def sub_parser(parser):
    sub_parser = parser.add_subparsers(
        title='Starfish command',
        description='Tool command',
        help='Tool command',
        dest='command'
    )
    return sub_parser

