__author__ = 'Lukas und Max K.'

class TagSearcher:
	tagConfigSet = Set()
	def __init__(self, tagConfigList):
		for configTag in tagConfigList:
			tagConfigSet.add(configTag)
	
	def containsDicomTagInConfig(dicomTag):	
		return dicomTag in tagConfigSet