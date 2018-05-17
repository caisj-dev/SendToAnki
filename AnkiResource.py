import json
import string
import re
# import asyncio
import requests
import  markdown2
# import items
# API_VERSION = 5
# API_URL     = 'http://localhost:8765'

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
		except requests.exceptions.ConnectionError:
			print('无法连接AnkiConnect端口，请安装该插件后重启Anki')
			return {}

		else:
			print(r.json())
			#return a dictionay
			print(type(r.json()))
			print('已连接Anki，正在处理结果...')
			return r.json()

	def addNote(self, params):
		if params:
			return self.makeRequest('addNote', params);

	# return all the model name in a dict
	def getModelNames(self):
		return self.makeRequest('modelNames');

	# return a model field in a dict
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

	def __init__(self, command, something=[]):
		# These command are based on the API of AnkiConnect
		# For more detail, see https://foosoft.net/projects/anki-connect/
		self.res = {}
		req_CMD ={
				1 : ['version',  	    {}],
				2 : ['sync',  			{}],
				3 : ['modelNames',      {}],
				4 : ['deckNames', 	    {}],
				# 'something' should be str type
				5 : ['modelFieldNames', { "modelName": something}],
				##'something' should be dict type
				6 : ['addNote',    	    { "note": something}],
				##'something' should be list type
				7 : ['canAddNotes', 	{ "notes": something}],
				8 : ['updateNoteFields',{ "notes": something}],
		}
		if command in req_CMD:
			action = req_CMD[command][0]
			params = req_CMD[command][1]
			self.res = self.make_a_request(action, params)
		else:
			self.res = {}

	def make_a_request(self, action, params):
		res = {}
		try:
			res = requests.post("http://127.0.0.1:8765", json = {'action': action,
																 'params': params,
																 'version': 5})
			res = res.json()
		except requests.exceptions.ConnectionError:
			print('无法连接AnkiConnect端口')
			return res
		else:
			if len(res) == 2:
				print('已连接Anki，正在处理结果...')
				return res

class Model:
	def __init__(self, name):
		#model name
		self.name   = name
		#model fields in a list
		self.fields = self.getFields()

	#return fields of a model
	def getFields(self):
		# params ={ "modelName": self.name}
		dic = Resource(3).res
		# print(modelFieldNameDict)
		if 'result' in dic:
			# print(modelNameDict.get('result'))
			li =  dic.get('result')
		return li


class Notes:
	def __init__(self, body):
		self.deck        = self.parseDeckName(body)
		self.model       = Model(self.parseModelName(body))
		self.fields_dict = self.parseTXT2Fields(body)
		self.tags_list   = self.parseTags(body)
		self.is_sent 	 = False
	# return body of note, dict
	def parseTXT2Fields(self, body):
		d = {}
		#pat =  '##{0}([.\n]+)##{0}|##([.\n]+)---'.format(field,field)
		for field in self.model.fields:
			# st = '##{0}\n([\s\S]+)##'.format(field)
			pat = re.compile(r'{0}'.format('##{0}\n([\s\S]+?)##'.format(field)))

			res = pat.search(body)
			if res != None:
				res = res.group(1)
				d[field] = markdown2.markdown(res, extras=["cuddled-lists"])
			else:
				# the last field
				st = '##{0}\n([\s\S]+?)\n======'.format(field)
				pat = re.compile(r'{0}'.format(st))
				res = pat.search(body)
				if res != None:
					res = res.group(1)
					d[field] = markdown2.markdown(res, extras=["cuddled-lists"])
				else:
					d[field] = ''
		return d
	# return model name from sublime text
	def parseModelName(self, body):
		pat = re.compile(r'{0}'.format('Model:([\s\S]+?)\n'))
		res_model = pat.search(body)
		if res_model != None:
			res_model = res_model.group(1)
		else:
			return ''
		return res_model

	def parseDeckName(self, body):
		pat = re.compile(r'{0}'.format('Deck:([\s\S]+?)\n'))
		res_deck = pat.search(body)
		if res_deck != None:
			res_deck = res_deck.group(1)
		else:
			return ''
		return res_deck

	#TODO： return list of tags
	def parseTags(self, body):
		res_tag = []
		pat = re.compile(r'{0}'.format('##Tags([\s\S]+?)##'))
		res = pat.search(body)
		if res != None:
			pat = re.compile(r',')
			res_spli = pat.split(res.group(1))

			res_tag = res_spli
		return res_tag

	def sendNote(self):
		# print('sendNote:'+self.deck)
		params = {
					'note':{
							'deckName' :self.deck,
							'modelName':self.model.name,
							'fields'   :self.fields_dict,
							'tags'     :self.tags_list
							}
				}
		r = AnkiResource()
		r.addNote(params)

		#if has non-empty string in result
		# if r.res.get('result'):
		# 	self.is_sent = True
		# 	print(r.res.get('result'))
		# 	print (bool(r.res.get('error')))


#creat new Template by the givin model and deck.
class Template:
	def __init__(self, deck, model):
		self.deck        = deck
		self.model       = model
		self.fields_list = Model(model).fields

	#return a template string.
	def new(self):
		# fields_list = self.model.fields
		print(len(self.fields_list))
		if len(self.fields_list) != 0:
			info_list = []
			info_list.append('Deck:'+ self.deck  )
			info_list.append('Model:'+ self.model )
			info_list.append('----------------------------\n')
			str  = '\n'
			info_string = str.join(info_list)

			body_list = []
			# add Tag
			body_list.append('##Tags')

			for field in self.fields_list:
				body_list.append('##' + field)
			body_list.append('============================\n')
			# seperate by two line, easy to read in MarkDown
			str  = '\n\n'
			note_string = str.join(body_list)

			note_string = info_string + note_string
			print(note_string)
			return note_string
		else:
			return ''
class NoteBook:
	def __init__(self, body):
		self.body = body

	def send(self):
		pat = re.compile(r'\n===========')
		res_spli = pat.split(self.body)
		leng = len(res_spli )
		print(leng)
		i = 0
		for a_note_str in res_spli:
			i += 1
			#discard the last item in res_spli
			if i == leng :
				break
			Notes(a_note_str).sendNote()

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
		info_list = []
		info_list.append('-----------------------')
		info_list.append('deck:'+ deckName  )
		info_list.append('Model:'+ modelName  )
		info_list.append('-----------------------\n')
		str  = '\n'
		mfStartString = str.join(info_list)

		body_list = []
		# #add Tag
		body_list.append('##Tag')
		for field in mfList:
			body_list.append('##'+field)
		body_list.append('------------------------\n')
		# seperate by two line, easy to read in MarkDown
		str  = '\n\n'
		note_string = str.join(body_list)

		note_string = mfStartString + note_string
		print(note_string)
		return note_string
		# mfList = info_list + body_list
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
		deckNameList = []
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
# # with urllib.request.urlopen(req) as res:
# #    the_page = res.read()
# # print(the_page)
# with urllib.request.urlopen(url,params) as res:
#     r = res.read() # Returns http.client.HTTPres.
# print(r)
