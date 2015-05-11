__author__ = 'UNKNOWN'

import sys
import os

from Parser import Parser
from TagSearcher import TagSearcher
from ConfigFileReader import ConfigFileReader
from TagExporter import TagExporter



# Wird als Programmeinstiegspunkt genutzt. Liest Verzeizeichispfad von Dicomdateien  ein, der mitgegeben wurde.
# Optional kann auch der Pfad zur Configdatei eingelesen werden.

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 Main.py <Attributefile> <Directory of dicom files> <Outputfile>")
        exit()

    attribute_file = sys.argv[1]
    dicom_directory = sys.argv[2]
    output_file = sys.argv[3]
    data = []
    exporter = TagExporter()
    configFileReader = ConfigFileReader()
    tagSearcher = TagSearcher(configFileReader.read_config(sys.argv[1]))

    for x in os.listdir(dicom_directory):
        if os.path.isfile(dicom_directory + x):
            data.append(dicom_directory + x)

    for x in data:
        print(x + ":")
        parsed = {}
        parsed = Parser().parse_dicom_file(tagSearcher, x)
        for key in parsed:
            exporter.saveTag(key, parsed[key], str(x).split("/")[-1])
            print(key + ": " + parsed[key])
        print("\n\n")

    exporter.writeToFile(output_file, configFileReader.read_config(attribute_file))
