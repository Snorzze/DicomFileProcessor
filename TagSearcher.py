__author__ = 'Lukas und Max K.'


class TagSearcher:
    tagConfigSet = set()

    def __init__(self, tag_config_list):
        for configTag in tag_config_list:
            self.tagConfigSet.add(configTag)

    def contains_dicom_tag_in_config(self, dicom_tag):
        return dicom_tag in self.tagConfigSet