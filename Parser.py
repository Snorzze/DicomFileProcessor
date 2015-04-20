__author__ = 'Max W. und Maja'

import sys

from TagSearcher import TagSearcher


class Parser:
    def parseDicomFile(self, tagSearcher, pathToDicomFile):
        f = open(pathToDicomFile, "rb")
        v1 = f.read(1)
        v2 = f.read(1)
        v3 = f.read(1)
        v4 = f.read(1)
        while len(v4) != 0:
            str1 = hex(ord(v1)).replace("0x", "")
            str2 = hex(ord(v2)).replace("0x", "")
            str3 = hex(ord(v3)).replace("0x", "")
            str4 = hex(ord(v4)).replace("0x", "")
            if len(str1) == 1:
                str1 = str(0) + str1
            if len(str2) == 1:
                str2 = str(0) + str2
            if len(str3) == 1:
                str3 = str(0) + str3
            if len(str4) == 1:
                str4 = str(0) + str4
            tagString = str(str1) + str(str2) + str(str3) + str(str4)
            print(tagString)
            if tagSearcher.containsDicomTagInConfig(tagString):
                print("Habe was gefunden")
                break
            else:
                v1 = v2
                v2 = v3
                v3 = v4
                v4 = f.read(1)


print("ENDE")

if __name__ == "__main__":
    Parser().parseDicomFile(TagSearcher(["98675412", "89A042B1", "00080016"]), sys.argv[1])
