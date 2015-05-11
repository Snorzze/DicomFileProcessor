import csv

class TagExporter:
    exportData = {}

    def saveTag(self, tag, value, file):
        if file not in self.exportData:
            self.exportData[file] = {}
        data = {"tag": tag, "value": value}
        self.exportData[file][tag] = data

    def writeToFile(self, f, tags):
        with open('names.csv', 'w') as csvfile:
            fieldnames = ['file'] + tags
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for filename, tagMap in self.exportData.items():
                row = self.generateTableRow(filename, tagMap, tags)
                writer.writerow(row)

    def generateTableRow(self, filename, tagMap, tags):
        row = {"file": filename}
        for tag in tags:
            value = "-"
            if tag in tagMap:
                 value = tagMap[tag]["value"]
            # Tag könnte hier gedreht werden zu besserer Lesbarkeit
            row[tag] = value

        return row
