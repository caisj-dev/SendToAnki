import json
import string
import re
# import asyncio
import requests
import  markdown2
# import items
API_VERSION = 5
API_URL     = 'http://localhost:8765'



class AnkiResource:
	def __init__(self):
		pass
	# sublime.error_message("Could not find a definition")
	def makeRequest(self, action, params={}):
		# request = json.dumps([ action, params ])
		try:
			r = requests.post("http://127.0.0.1:8765", json=
												{
												    "action": action,
												    "version": 5,
												    "params": params
												}
						)
		except ConnectionRefusedError:
			return None

		else:
			print(r.json())
			#return a dictionay
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

class Resource:
	def __init__(self, action, params={}):
		try:
			self.response = requests.post(API_URL, json = self.request(action, params))
			self.response = self.response.json()
		except requests.exceptions.ConnectionError:
			print('无法连接AnkiConnect端口，请安装该插件后重启Anki')
			self.response = {}
		else:
			# print(self.response)
			if len(self.response) == 2:
				print('请求成功，正在处理结果...')

	def request(self, action, params):
		return {'action': action, 'params': params, 'version': API_VERSION}

class Model:
	def __init__(self, name):
		#model name
		self.name = name
		#model fields in a list
		self.fields = self.getFields()
		#model content in a dictionary
		# self.content = self.getFieldsCotent()

	#return fields of a model
	def getFields(self):
		params = {"modelName": self.name}
		r = Resource('modelFieldNames', params)
		if r.response != {}:
			return r.response.get('result')
		else:
			return []
	def printfields(self):
		for field in self.fields:
			print(field)

class Notes:
	def __init__(self, deck, model, content, tags):
		self.model = model
		self.fields_dict = initFields(model, content)
		self.deck = deck
		self.tags = tags

	def initFields(self, model, content):
		#new a dict that store each field's content
		field = dict()
		for field in self.model.fields:
			d[field] = newContent_fromcontent
		return field

	def sendNote(self):
		note = {'note':{'deckName':self.deck,
						'modelName':self.model,
						'fields':self.fields_dict,
						'tags':self.tags
						}
				}

		r = Resource('addNote', note)
		if r.response != {}:
			return r.response.get('result')

class Note:
	def __init__(self):
		pass

	##Temp method
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
	def cardModel2MarkdowndSyntax( modelName,deckName):
		mfList =MyHelper.parseCardModelFields2List(modelName)
		mfStartList = []
		mfStartList.append('-----------------------')
		mfStartList.append('deck:'+ deckName  )
		mfStartList.append('Model:'+ modelName  )
		mfStartList.append('-----------------------\n')
		str  = '\n'
		mfStartString = str.join(mfStartList)

		mfListTemp = []
		# #add Tag
		mfListTemp.append('##Tag')
		for field in mfList:
			mfListTemp.append('##'+field)
		mfListTemp.append('------------------------\n')
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
         #parse the model name from Anki resource to string format
	def parseModelName2List():
		modelNameDict = AnkiResource().getModelNames()
		# for key,values in  ModelNamedict.items():
		if 'result' in modelNameDict:
			#get the list
			modelNameList=  modelNameDict.get('result')
		return modelNameList

	#parse the deck name from Anki resource to string format
	def parseDeckName2List():
		deckNameDict = AnkiResource().getDeckNames()
		# for key,values in  ModelNamedict.items():
		if 'result' in deckNameDict:
			deckNameList=  deckNameDict.get('result')
		return deckNameList
	# example:
	#modelName ='知识点-Mix (Leaflyer)'
	def parseCardModelFields2List(modelName):
		params ={ "modelName": modelName}
		modelFieldNameDict = AnkiResource().getModelFieldNames(params)
		# print(modelFieldNameDict)
		if 'result' in modelFieldNameDict:
			# print(modelNameDict.get('result'))
			modelFieldNameList=  modelFieldNameDict.get('result')
		return modelFieldNameList
	#check if the current line is Field Name
	def isMDFieldLine(MDLine):
		patStartSign = re.compile(r'^[#]{2}')
		if patStartSign.match( MDLine):
			return True
		else:
			return False
	#parse  field name of MD  syntax into field name string
	def parseMDFieldName(MDLine):

		patStartSign = re.compile(r'^[#]{2}(.*)')
		fieldname = patStartSign.match(MDLine).group(1)
		print(type(fieldname))
		return fieldname

	#parse the Mmodelname of the note, return model name in string
	def parseMDCardInfo(MDLine):
		patStartSign = re.compile(r'^model:(.*)')
		modelName = patStartSign.match(MDLine).group(1)
		# print(modelName)
		return modelName


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
