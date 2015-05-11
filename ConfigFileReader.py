__author__ = 'Thomas and Kemal and Lukas'


class ConfigFileReader:
    def read_config(self, path):
        self.content = self.read_config_correct_order(path)
        return list(map(self.turn, self.content))

    def turn(self, tag):
        group_id = self.swap(tag[:-4])
        element_id = self.swap(tag[-4:])
        return group_id + element_id

    @staticmethod
    def swap(tag_half):
        part1 = tag_half[:-2]
        part2 = tag_half[-2:]
        return part2 + part1

    @staticmethod
    def read_config_correct_order(path):
        text_file = open(path, "r")
        return text_file.read().strip().split(",")
