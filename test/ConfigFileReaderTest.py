import unittest
import os

from ConfigFileReader import ConfigFileReader


path = "./ConfigSamples/configSample1.txt"

directory = os.path.dirname(__file__)
path = os.path.join(directory, path)

fileOrderTags = ['18005011', '18005111', '18005211']
correctOrder = ['00181150', '00181151', '00181152']


class TestConfigFileReader(unittest.TestCase):
    def setUp(self):
        self.configFileReader = ConfigFileReader()

    def test_read_config(self):
        result = self.configFileReader.read_config(path)
        self.assertEquals(result, fileOrderTags)
        self.assertEquals(self.configFileReader.content, correctOrder)

    def test_read_config_correct_order(self):
        result = self.configFileReader.read_config_correct_order(path)
        self.assertEquals(result, correctOrder)


if __name__ == "__main__":
    unittest.main()