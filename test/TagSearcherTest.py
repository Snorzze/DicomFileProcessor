import unittest

from TagSearcher import TagSearcher


configTagList = ["98675412", "89A042B1", "11457863"]


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.tagSearcher = TagSearcher(configTagList)

    def test_valid_instance(self):
        self.assertIsInstance(self.tagSearcher, TagSearcher)

    def test_contains_tag(self):
        self.assertTrue(self.tagSearcher.containsDicomTagInConfig(configTagList[0]))
        self.assertTrue(self.tagSearcher.containsDicomTagInConfig(configTagList[1]))
        self.assertTrue(self.tagSearcher.containsDicomTagInConfig(configTagList[2]))

    def test_should_not_contain_tag(self):
        self.assertFalse(self.tagSearcher.containsDicomTagInConfig("0123"))


if __name__ == '__main__':
    unittest.main()