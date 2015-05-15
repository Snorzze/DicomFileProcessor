import csv


class TagExporter:
    exportData = {}

    def save_tag(self, tag, value, file):
        if file not in self.exportData:
            self.exportData[file] = {}
        data = {"tag": tag, "value": value}
        self.exportData[file][tag] = data

    def write_to_file(self, f, tags):
        with open(f, 'w') as csv_file:
            fieldnames = ['file'] + tags
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for filename, tagMap in self.exportData.items():
                row = self.generate_table_row(filename, tagMap, tags)
                writer.writerow(row)

    @staticmethod
    def generate_table_row(filename, tag_map, tags):
        row = {"file": filename}
        for tag in tags:
            value = "-"
            if tag in tag_map:
                value = tag_map[tag]["value"]
            # Tag könnte hier gedreht werden zu besserer Lesbarkeit
            row[tag] = value

        return row
