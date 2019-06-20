"""

    Tests for `squid-py issues`.

"""


from tests.integration.squid_issues.example_config import ExampleConfig
from squid_py import Ocean
from squid_py import ConfigProvider

def test_config_setup_working():
    config = ExampleConfig.get_config()
    ConfigProvider.set_config(config)
    ocn = Ocean()

def test_config_setup():

    config = ExampleConfig.get_config()
    ocn = Ocean(config)
