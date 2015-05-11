__author__ = 'Kurscheidt & Schmidt'

import unittest
import os

from Parser import Parser
from TagSearcher import TagSearcher

filepath = "../ExampleFiles/brain_001.dcm"

dir = os.path.dirname(__file__)
filepath = os.path.join(dir, filepath)

resultdata = {"08007000": "GE Medical Systems", "08003300": "143006", "08001010": "MRS1"}


def get_tags():
    result = []
    for tag in resultdata.items():
        result.append(tag[0])
    return result


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse(self):
        parsed_result = self.parser.parse_dicom_file(TagSearcher(get_tags()), filepath)
        for tag in get_tags():
            self.assertEqual(resultdata[tag], parsed_result[tag])

    def test_should_not_find_tag(self):
        tag = "00889777"
        parsed_result = self.parser.parse_dicom_file(TagSearcher([tag]), filepath)
        self.assertFalse(tag in parsed_result)


if __name__ == '__main__':
    unittest.main()
