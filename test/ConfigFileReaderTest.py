import unittest

import ConfigFileReader

path = "ConfigSamples/configSample1.txt"

class TestConfigFileReader(unittest.TestCase):
    def setUp(self):
        self.configFileReader = ConfigFileReader()

    def test_readConfig(self):
        result = self.readConfig(path)
        validResult = ['18005011', '18005111', '18005211']
        self.assertEquals(result, validResult)

if __name__ == "__main__":
    unittest.main()