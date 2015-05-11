import unittest

from ConfigFileReader import ConfigFileReader

path = "/ConfigSamples/configSample1.txt"

fileOrderTags = ['18005011', '18005111', '18005211']
correctOrder = ['00181150', '00181151', '00181152']

class TestConfigFileReader(unittest.TestCase):
    def setUp(self):
        self.configFileReader = ConfigFileReader()

    def test_readConfig(self):
        result = self.configFileReader.readConfig(path)
        self.assertEquals(result, fileOrderTags)
        self.assertEquals(self.configFileReader.content, correctOrder)

    def test_readConfigCorrectOrder(self):
        result = self.configFileReader.readConfigCorrectOrder(path)
        self.assertEquals(result, correctOrder)


if __name__ == "__main__":
    unittest.main()