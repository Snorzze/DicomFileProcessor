__author__ = 'Max Westers'

import sys
import os

from Parser import Parser
from TagSearcher import TagSearcher
from ConfigFileReader import ConfigFileReader
from TagExporter import TagExporter
from ShiftError import ShiftError


# Wird als Programmeinstiegspunkt genutzt. Liest Verzeizeichispfad von Dicomdateien  ein, der mitgegeben wurde.
# Optional kann auch der Pfad zur Configdatei eingelesen werden.

def print_documentation():
    print("\n################################## DOCUMENTATION #####################################")
    print("\nUsage: python3 Main.py <Directory of dicomfiles> (<Outputfile>) (<Attributefile>)")
    print("\nAttributes:")
    print("Directory of dicomfiles:")
    print("\tThe Folder with all dicomfiles. This folder should just contains dicomfiles or folders.")
    print("\tOther files will produce an error.")
    print("\nOutputfile")
    print("\tThe output file, which contains all found datas from the dicomfiles. This is an optional")
    print("\tparameter. If not setted, the output file will be generated in the dicomfile directory")
    print("\tnamed \"output.csv\"")
    print("\nAttributefile")
    print("\tThe file which contains all Attributes which should be picked out. This is an optional")
    print("\tparameter. If not setted, the standard attribute file will be used (./attributes.txt). ")
    print("\nFor using a standard parameter but also changing an other parameter after it, you can")
    print("use - for the standard parameter. For example:")
    print("\n\tpython3 Main.py ./dicomFiles/ - ./attributs.txt")
    print("\n######################################################################################\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_documentation()
        exit()

    dicom_directory = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else dicom_directory + "output.csv"
    attribute_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else "./attributes.txt"
    data = []
    exporter = TagExporter()
    config_file_reader = ConfigFileReader()
    tag_searcher = TagSearcher(config_file_reader.read_config(attribute_file))

    for x in os.listdir(dicom_directory):
        if os.path.isfile(dicom_directory + x):
            data.append(dicom_directory + x)

    for x in data:
        print("Lese " + str(x).split("/")[-1])
        parsed = {}
        try:
            parsed = Parser().parse_dicom_file(tag_searcher, x)
        except ShiftError as e:
            print("Konnte Tag nicht parsen, da die angegebene"
                  " Länge (" + str(e.msg) + ") des Wertes die gesamte Dateigröße überschreitet!"
                  " Datei ist Fehlerhaft.")
        for key in parsed:
            exporter.save_tag(key, parsed[key], str(x).split("/")[-1])

    exporter.write_to_file(output_file, config_file_reader.read_config(attribute_file))
    print("\nWrote file to " + output_file)
    print("\nFINISHED!")