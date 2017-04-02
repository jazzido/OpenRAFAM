import unittest, os

from rafam_extract import config

class ConfigTest(unittest.TestCase):
    def test_read_config(self):
        f = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         'fixtures/config.ini')
        c = config.read_config(f)
        assert c == {'Database': {'username': 'foo', 'host': 'example.com', 'password': 'bar', 'sid': 'MBAHIA'}}
