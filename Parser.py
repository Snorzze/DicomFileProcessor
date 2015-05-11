__author__ = 'Max W. und Maja'

import struct


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

    # NUR BIS PIXEL DATA SUCHEN ( 7FE0,0010 )

    def parse_dicom_file(self, tagsearcher, pathtodicomfile):
        """
        Parses the given dicom file for the tags, the tagsearcher includes
        :param tagsearcher: includes the searched tags
        :param pathtodicomfile: the path to the dicomdata
        :return: a hasmap with all found tags as key and values
        """

        self.file = open(pathtodicomfile, "rb")
        if self.find_dicom_start():
            export_map = {}
            tag = self.shift_byte_sequence(4)
            while tag is not None:
                if tag == self.dicomImageStartTag:
                    return export_map
                if tagsearcher.containsDicomTagInConfig(tag):
                    export_map[tag] = self.get_actual_tag_value()
                else:
                    self.skip_actual_tag()

                tag = self.shift_byte_sequence(4)

            return export_map
        else:
            print("Konnte Starttag von Datei nicht finde. Datei ist fehlerhaft!")
            return {}

    def get_actual_tag_value(self):
        self.shift_byte_sequence(4)
        if self.is_valid_vr():
            # Going for explicite Value --> little endian
            if not self.is_special_vr():
                # Normal vr --> normal process
                lenght = struct.unpack("<H", (self.v3 + self.v4))[0]
                return self.get_byte_sequence_as_ascii(lenght)
            else:
                # Specail vr --> special process
                # skip reservated 2 bytes
                self.shift_byte_sequence(4)
                # read special lenght to read
                lenght = struct.unpack("<I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
                return self.get_byte_sequence_as_ascii(lenght)
        else:
            # Going for implicit Value --> big endian
            lenght = struct.unpack(">I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
            return self.get_byte_sequence_as_ascii(lenght)

    def skip_actual_tag(self):
        self.shift_byte_sequence(4)
        if self.is_valid_vr():
            # Going for explicit Value --> little endian
            if not self.is_special_vr():
                # Normal vr --> normal process
                lenght_to_skip = struct.unpack("<H", (self.v3 + self.v4))[0]
                self.shift_byte_sequence(lenght_to_skip)
            else:
                # Specail vr --> special process
                # skip reservated 2 bytes and go to new length size
                self.shift_byte_sequence(4)
                # read special lenght to skip
                lenght_to_skip = struct.unpack("<I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
                self.shift_byte_sequence(lenght_to_skip)
        else:
            # Going for implicit Value --> big endian
            lenght_to_skip = struct.unpack(">I", (self.v1 + self.v2 + self.v3 + self.v4))[0]
            self.shift_byte_sequence(lenght_to_skip)

    def shift_byte_sequence(self, lengthofnewbytes):
        """
        Shifts the filereader for the given length.

        :param lengthofnewbytes: the length to shift
        :return: the last four bytes as string
        """

        while lengthofnewbytes > 0:
            self.v1 = self.v2
            self.v2 = self.v3
            self.v3 = self.v4
            self.v4 = self.file.read(1)
            lengthofnewbytes -= 1

        if len(self.v4) != 0:
            return self.generate_actual_byte_sequence_as_string()
        else:
            return None

    def get_byte_sequence_as_ascii(self, length):
        """
        Reads the length of bytes and returns the ascii converted string

        :param length: the lenght of the value to read
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
        bytesequence = self.shift_byte_sequence(4)
        while bytesequence is not None:
            if bytesequence == self.dicomStartBytePath:
                return True
            else:
                bytesequence = self.shift_byte_sequence(1)
        return False

    def is_valid_vr(self):
        vr = self.convert_hex_to_ascii(self.v1) + self.convert_hex_to_ascii(
            self.v2)
        validvrs = set(
            ["AE", "AS", "AT", "CS", "DA", "DS", "DT", "FL", "FD", "IS", "LO", "LT", "OB", "OF", "OW", "PN", "SH",
             "SL",
             "SQ", "SS", "ST", "TM", "UI", "UL", "UN", "US", "UT"])
        return vr in validvrs

    def is_special_vr(self):
        vr = self.convert_hex_to_ascii(self.v1) + self.convert_hex_to_ascii(
            self.v2)
        specialvrs = set(["OB", "OW", "SQ", "UN"])
        return vr in specialvrs

    @staticmethod
    def convert_hex_to_string(hex_value):
        return hex(ord(hex_value)).replace("0x", "")

    @staticmethod
    def convert_hex_to_ascii(hex_value):
        try:
            return bytes.fromhex(Parser.convert_hex_to_string(hex_value)).decode('utf-8')
        except ValueError:
            return Parser.convert_hex_to_string(hex_value)

