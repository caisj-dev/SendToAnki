import json
import string
import re
# import asyncio
import requests
import  markdown2
# import items
class AnkiResource:
	def __init__(self):
		pass

	def makeRequest(self, action, params={}):
		# request = json.dumps([ action, params ])
		r = requests.post("http://127.0.0.1:8765", json=
												{
												    "action": action,
												    "version": 5,
												    "params": params
												}
						)
		print(r.json())
		
		print(type(r.json()))
		return r.json()
	#添加Card=Note
	def addNote(self, params):
		if params:
			return self.makeRequest('addNote', params);

	# 所有模板名
	def getModelNames(self):
		return self.makeRequest('modelNames');

	# 某个模板的所有field
	def getModelFieldNames(self, params): 
# 		params ={ "modelName":'知识点-Mix (Leaflyer)'}
#		x.getModelFieldNames(params)
		return self.makeRequest('modelFieldNames', params);
	# Version
	def getVersion(self,params):
	# return self.makeRequest('version');
		return self.makeRequest(params);

	def getDeckNames(self):
	# return self.makeRequest('version');
		return self.makeRequest('deckNames');
	
class Note:
	def __init__(self):
		pass
		
	def add(  deckName, modelName, question, answer, tags) :
		# self.deckName = deckName
		# self.modelName = modelName
		# self.question = question
		# self.answer = answer
		note = {'note':{'deckName':deckName,
						'modelName':modelName,
						'fields':{
							'问题': question,
							'答案': answer,
							'笔记': '',
							'相关知识': ''
							},
						'tags':tags
						}
				}
		r = AnkiResource()
		r.addNote(note)
	
	
	#Convert card model in dict format into MdSyntax
	# its format is customazed.
	# below is the example of Markdown syntax coresponding fields in one of my Anki models:
		##Question

		##Ansewer

		##Note

		##Other  Knowledge
	def cardModel2MarkdowndSyntax( modelName):
		mfList =MyHelper.ParseCardModelFields2List(modelName)
		mfStartList = []
		mfStartList.append('*****')
		mfStartList.append('Model:'+ modelName + '\n' )
		
		mfStartList.append('*****\n')
		str  = '\n'
		mfStartString = str.join(mfStartList)

		mfListTemp = []
		# #add Tag
		mfListTemp.append('##Tag')
		for field in mfList:
			mfListTemp.append('##'+field)
		# seperate by two line, easy to read in MarkDown
		str  = '\n\n'
		mfString = str.join(mfListTemp)

		mfString = mfStartString + mfString
		print(mfString)
		return mfString
		# mfList = mfStartList + mfListTemp
# c = Card('deck','le','Q','A')
class MyHelper:
	def isQusetionSyntax(line):
		# if re.match(r'^[#][^#]', line):
		if re.match(r'^[#]{2}[Q]', line):
			return True
		else:
			return False

	def isAnswerSyntax(line):
		if re.match(r'^[#]{2}[A]', line):
			return True
		else:
			return False
	def isTagSyntax(line):
		if re.match(r'^[#]{2}[T][A][G]', line):
			return True
		else:
			return False
#parse the model name from Anki resource.
	def ParseCardModelName2List():
		modelNameDict = AnkiResource().getModelNames()
		# for key,values in  ModelNamedict.items():
		if 'result' in modelNameDict:
			# print(modelNameDict.get('result'))
			modelNameList=  modelNameDict.get('result')
			# print(type(modelNameList))
		return modelNameList

	# example:  
	#modelName ='知识点-Mix (Leaflyer)'
	def ParseCardModelFields2List(modelName):
		params ={ "modelName": modelName}
		modelFieldNameDict = AnkiResource().getModelFieldNames(params)
		# print(modelFieldNameDict)
		# print(type(modelFieldNameDict))
		if 'result' in modelFieldNameDict:
			# print(modelNameDict.get('result'))
			modelFieldNameList=  modelFieldNameDict.get('result')
		return modelFieldNameList


class ForTest:
	def ModelNameList ():
		aList= ['abc','efg','bcg']
		#print list string
		print('[%s]' % ', '.join(map(str, aList)))
		return aList


# a = markdown2.markdown("*boo!*", extras=["footnotes"])
# print (a)
	
	# def GenStringList(N):
	# 	Q = '#23'
	# 	A = '##dss'
	# 	L = ArrayList(range(N))
	# 	for i in range(1,N):
	# 		L.add(i, Q)
	# 		L.add(i, A)
	# 	return L
		
# print(Helper.GenStringList(6))

# a = '##12'#Q F,A T
# c = '#22' #Q T,A F
# b = '321#'
# print(MyHelper.isQusetionSyntax(a))
# print(MyHelper.isAnswerSyntax(a))
# print(MyHelper.isQusetionSyntax(b))
# print(MyHelper.isAnswerSyntax(b))



# x = AnkiResource()
# x.getModelNames()
# params ={'modelName':'Basic'}
# x.getModelFieldNames(params)
# params = Note
# # x.getDeckNames()
# x.addNote(Note)
# # print(json.dumps(Note))


# # Request.add_data(values)
# # data = urllib.parse.urlencode(values)
# # # data = data.encode('ascii') # data should be bytes
# # req = urllib.request.Request(url, values)
# # with urllib.request.urlopen(req) as response:
# #    the_page = response.read()
# # print(the_page)
# with urllib.request.urlopen(url,params) as response:
#     r = response.read() # Returns http.client.HTTPResponse.
# print(r)
