__author__ = 'Lukas und Max K.'

class TagSearcher:
	tagConfigSet = set()
	def __init__(self, tagConfigList):
		for configTag in tagConfigList:
			self.tagConfigSet.add(configTag)
	
	def containsDicomTagInConfig(self, dicomTag):	
		return dicomTag in self.tagConfigSet