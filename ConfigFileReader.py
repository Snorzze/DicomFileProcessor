__author__ = 'Thomas and Kemal and Lukas'

class ConfigFileReader:

    def readConfig(self, path):
        text_file = open(path, "r")
        content = text_file.read().strip().split(",")
        return list(map(self.turn, content))

    def turn(self, tag):
        groupId = self.swap(tag[:-4])
        elementId = self.swap(tag[-4:])
        return groupId + elementId

    def swap(self, tagHalf):
        part1 = tagHalf[:-2]
        part2 = tagHalf[-2:]
        return part2 + part1