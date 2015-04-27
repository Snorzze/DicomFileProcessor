__author__ = 'Max W. und Maja'

import sys, struct

from TagSearcher import TagSearcher


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
        self.file = open(pathtodicomfile, "rb")
        if self.find_dicom_start():
            export_map = {}
            print("Dicom Starttag von Datei gefunden. Beginne parsen...")
            tag = self.shift_byte_sequence(4)
            while tag is not None:
                if tag == self.dicomImageStartTag:
                    print("Datei erfolgreich beendet!")
                    break
                if tagsearcher.containsDicomTagInConfig(tag):
                    export_map[tag] = self.get_actual_tag_value()
                    print(export_map[tag])
                else:
                    self.skip_actual_tag()

                tag = self.shift_byte_sequence(4)

            print("[DONE]")
        else:
            print("Konnte Starttag von Datei nicht finde. Datei ist fehlerhaft!")

    def get_actual_tag_value(self):
        self.shift_byte_sequence(4)
        vr = self.convert_hex_to_ascii(self.v1) + self.convert_hex_to_ascii(self.v2)
        if Parser.is_valid_vr(vr):
            # Going for explicite Value --> little endian
            lenght = struct.unpack("<H", (self.v3 + self.v4))[0]
            return self.get_byte_sequence(lenght)
        else:
            print("IMPLIZIT!!! NICHT FUNKTIONSFÄHIG")
            # Going for implicite Value --> big endian
            lenght = struct.unpack(">H", (self.v1 + self.v2 + self.v3 + self.v4))[0]
            return self.get_byte_sequence(lenght)

    def skip_actual_tag(self):
        temp = self.generate_actual_byte_sequence_as_string()
        self.shift_byte_sequence(4)
        vr = self.convert_hex_to_ascii(self.v1) + self.convert_hex_to_ascii(self.v2)
        if Parser.is_valid_vr(vr):
            # Going for explicite Value --> little endian
            lenght_to_skip = struct.unpack("<H", (self.v3 + self.v4))[0]
            self.shift_byte_sequence(lenght_to_skip)
            if temp == "02000100":
                print("ACHTUNG: Temporärer tag wird übersprungen! Nicht in Produktionsphase benutzen!")
                self.shift_byte_sequence(6)
        else:
            # Going for implicite Value --> big endian
            lenght_to_skip = struct.unpack(">H", (self.v1 + self.v2 + self.v3 + self.v4))[0]
            print(lenght_to_skip)
            self.shift_byte_sequence(lenght_to_skip)

    def shift_byte_sequence(self, lengthofnewbytes):
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

    def get_byte_sequence(self, length):
        string = ""
        while length > 0:
            self.shift_byte_sequence(1)
            string += self.convert_hex_to_string(self.v4)
            length -= 1
        return string

    def generate_actual_byte_sequence_as_string(self):
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


    @staticmethod
    def convert_hex_to_string(hex_value):
        return hex(ord(hex_value)).replace("0x", "")

    @staticmethod
    def convert_hex_to_ascii(hex_value):
        return bytes.fromhex(Parser.convert_hex_to_string(hex_value)).decode('utf-8')


    @staticmethod
    def is_valid_vr(vrtotry):
        validVRs = set(
            ["AE", "AS", "AT", "CS", "DA", "DS", "DT", "FL", "FD", "IS", "LO", "LT", "OB", "OF", "OW", "PN", "SH", "SL",
             "SQ", "SS", "ST", "TM", "UI", "UL", "UN", "US", "UT"])
        return vrtotry in validVRs


if __name__ == "__main__":
    Parser().parse_dicom_file(TagSearcher(["08002200"]), sys.argv[1])
