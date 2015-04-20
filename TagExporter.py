import csv

class TagExporter:
    exportData = {}

    def saveTag(self, tag, value, file):
        if tag not in self.exportData:
            self.exportData[tag] = []
        data = {"value": value, "file": file}
        self.exportData[tag].append(data)
