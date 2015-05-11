__author__ = 'Kurscheidt & Schmidt'

import unittest
import os

from Parser import Parser
from TagSearcher import TagSearcher


file_path = "../ExampleFiles/brain_001.dcm"

directory = os.path.dirname(__file__)
file_path = os.path.join(directory, file_path)

result_data = {"08007000": "GE Medical Systems", "08003300": "143006", "08001010": "MRS1"}


def get_tags():
    result = []
    for tag in result_data.items():
        result.append(tag[0])
    return result


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse(self):
        parsed_result = self.parser.parse_dicom_file(TagSearcher(get_tags()), file_path)
        for tag in get_tags():
            self.assertEqual(result_data[tag], parsed_result[tag])

    def test_should_not_find_tag(self):
        tag = "00889777"
        parsed_result = self.parser.parse_dicom_file(TagSearcher([tag]), file_path)
        self.assertFalse(tag in parsed_result)


if __name__ == '__main__':
    unittest.main()
