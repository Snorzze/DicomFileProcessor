__author__ = 'Max W. und Maja'

import struct
import os

from ShiftError import ShiftError

class Parser:
    def __init__(self):
        pass

    dicomStartBytePath = "4449434d"
    dicomImageStartTag = "e07f1000"
    v1 = None
    v2 = None
    v3 = None
    v4 = None
    file = None
    filesize = None

    # NUR BIS PIXEL DATA SUCHEN ( 7FE0,0010 )

    def parse_dicom_file(self, tag_searcher, path_to_dicom_file):
        """
        Parses the given dicom file for the tags, the tag_searcher includes

        :param tag_searcher: includes the searched tags
        :param path_to_dicom_file: the path to the dicom data
        :return: a hash map with all found tags as key and values
        """

        self.file = open(path_to_dicom_file, "rb")
        self.filesize = os.path.getsize(pathtodicomfile)
        if self.find_dicom_start():
            export_map = {}
            tag = self.shift_byte_sequence(4)
            while tag is not None:
                if tag == self.dicomImageStartTag:
                    return export_map
                if tag_searcher.contains_dicom_tag_in_config(tag):
                    export_map[tag] = self.get_actual_tag_value()
                else:
                    self.skip_actual_tag()

                tag = self.shift_byte_sequence(4)

            return export_map
        else:
            print("Konnte Starttag von Datei nicht finde. Datei ist fehlerhaft!")
            return {}

    def get_actual_tag_value(self):
        """
        Reads automatically the value of the current loaded tag

        :return: the value as string
        """

        self.shift_byte_sequence(4)
        if self.is_valid_vr():
            # Going for explicit Value --> little endian
            if not self.is_special_vr():
                # Normal vr --> normal process
                length = struct.unpack("<H", (self.v3 + self.v4))[0]
                return self.get_byte_sequence_as_ascii(length)
            else:
                # Special vr --> special process
                # skip reserved 2 bytes
                self.shift_byte_sequence(4)
                # read special length to read
                length = struct.unpack("<I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
                return self.get_byte_sequence_as_ascii(length)
        else:
            # Going for implicit Value --> big endian
            length = struct.unpack(">I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
            return self.get_byte_sequence_as_ascii(length)

    def skip_actual_tag(self):
        """
        Skips actual loaded tag automatically. Reads length and loads new bytes to the end of the value.
        After execution of this method, the last four bytes from the tag value are loaded in the variables.
        """

        self.shift_byte_sequence(4)
        if self.is_valid_vr():
            # Going for explicit Value --> little endian
            if not self.is_special_vr():
                # Normal vr --> normal process
                length_to_skip = struct.unpack("<H", (self.v3 + self.v4))[0]
                self.shift_byte_sequence(length_to_skip)
            else:
                # Special vr --> special process
                # skip reserved 2 bytes and go to new length size
                self.shift_byte_sequence(4)
                # read special length to skip
                length_to_skip = struct.unpack("<I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
                self.shift_byte_sequence(length_to_skip)
        else:
            # Going for implicit Value --> big endian
            length_to_skip = struct.unpack(">I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
            self.shift_byte_sequence(length_to_skip)

    def shift_byte_sequence(self, length_of_new_bytes):
        """
        Shifts the file reader for the given length.

        :param length_of_new_bytes: the length to shift
        :return: the last four bytes as string
        """

        while length_of_new_bytes > 0:
        if lengthofnewbytes > self.filesize:
            raise ShiftError(lengthofnewbytes)
        while lengthofnewbytes > 0:
            self.v1 = self.v2
            self.v2 = self.v3
            self.v3 = self.v4
            self.v4 = self.file.read(1)
            length_of_new_bytes -= 1

        if len(self.v4) != 0:
            return self.generate_actual_byte_sequence_as_string()
        else:
            return None

    def get_byte_sequence_as_ascii(self, length):
        """
        Reads the length of bytes and returns the ascii converted string

        :param length: the length of the value to read
        :return: the converted string
        """

        string = ""
        while length > 0:
            self.shift_byte_sequence(1)
            string += self.convert_hex_to_ascii(self.v4)
            length -= 1
        return string

    def generate_actual_byte_sequence_as_string(self):
        """
        Generates string from actual Hex-Bytes

        :return: generated string
        """

        str1 = hex(ord(self.v1)).replace("0x", "")
        str2 = hex(ord(self.v2)).replace("0x", "")
        str3 = hex(ord(self.v3)).replace("0x", "")
        str4 = hex(ord(self.v4)).replace("0x", "")
        if len(str1) == 1:
            str1 = str(0) + str1
        if len(str2) == 1:
            str2 = str(0) + str2
        if len(str3) == 1:
            str3 = str(0) + str3
        if len(str4) == 1:
            str4 = str(0) + str4
        return str(str1) + str(str2) + str(str3) + str(str4)

    def find_dicom_start(self):
        """
        Reads the data till the dicom starttag is found!
        
        :return: If the tag was found
        """

        byte_sequence = self.shift_byte_sequence(4)
        while byte_sequence is not None:
            if byte_sequence == self.dicomStartBytePath:
                return True
            else:
                byte_sequence = self.shift_byte_sequence(1)
        return False

    def is_valid_vr(self):
        """
        Checks if the vr is a valid vr
        :return: if vr is valid
        """

        vr = self.convert_hex_to_ascii(self.v1) + self.convert_hex_to_ascii(
            self.v2)
        valid_vrs = set(
            ["AE", "AS", "AT", "CS", "DA", "DS", "DT", "FL", "FD", "IS", "LO", "LT", "OB", "OF", "OW", "PN", "SH",
             "SL", "SQ", "SS", "ST", "TM", "UI", "UL", "UN", "US", "UT"])
        return vr in valid_vrs

    def is_special_vr(self):
        """
        Checks if vr is special vr, which has to read on a special way:
            - Skipping 2 bytes which are reserved for further dicom standards
            - Reading 4 unsigned little endian Integers

        :return: if vr is a special vr
        """

        vr = self.convert_hex_to_ascii(self.v1) + self.convert_hex_to_ascii(
            self.v2)
        special_vrs = set(["OB", "OW", "SQ", "UN"])
        return vr in special_vrs

    @staticmethod
    def convert_hex_to_string(hex_value):
        """
        :param hex_value: the byte to convert
        :return: the bytes as string without 0x
        """

        return hex(ord(hex_value)).replace("0x", "")

    @staticmethod
    def convert_hex_to_ascii(hex_value):
        """
        Converts a hex value to a ascii encoded string
        :param hex_value: the value to encode
        :return: the encode value or, if it wasn't a convertible hex-byte the byte as string
        """

        try:
            return bytes.fromhex(Parser.convert_hex_to_string(hex_value)).decode('utf-8')
        except ValueError:
            return Parser.convert_hex_to_string(hex_value)

