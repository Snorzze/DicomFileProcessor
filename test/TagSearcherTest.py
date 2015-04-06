import unittest

from TagSearcher import TagSearcher


configTagList = ["98675412", "89A042B1", "11457863"]

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.tagSearcher = TagSearcher(configTagList)

    def test_valid_instace(self):
        self.assertIsInstance(self.tagSearcher, TagSearcher)
        print("test_valid_instance")

    def test_contains_tag(self):
        tag = configTagList[1]
        self.assertTrue(self.tagSearcher.containsDicomTagInConfig(tag))
        self.assertTrue(self.tagSearcher.containsDicomTagInConfig(configTagList[0]))
        print("test_contains_tag")

    def test_should_not_contain_tag(self):
        self.assertFalse(self.tagSearcher.containsDicomTagInConfig("0123"))
        print("test_should_not")

if __name__ == '__main__':
    unittest.main()