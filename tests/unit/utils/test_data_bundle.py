"""

Test utils.data_bundle module



"""
import math

from starfish.utils.data_bundle import decode_readable_size

ONE_TB = math.pow(1024, 4)
ONE_GB = math.pow(1024, 3)
ONE_MB = math.pow(1024, 2)
ONE_KB = 1024


def test_decode_readable_size():

    test_values = {
        '1mb': ONE_MB,
        '1 mb': ONE_MB,
        '125mb': ONE_MB * 125,
        '2m': ONE_MB * 2,
        '1kb': ONE_KB,
        '20.2kb': ONE_KB * 20.2,
        '4k': ONE_KB * 4,
        '502GB': ONE_GB * 502,
        '6G': ONE_GB * 6,
        '22T': ONE_TB * 22,
        '1 Tb': ONE_TB
    }
    for text, actual_value in test_values.items():
        value = decode_readable_size(text)
        print(text)
        assert(value == int(actual_value))

