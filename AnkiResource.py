import json
import string
import re
# import asyncio
import requests
import  markdown2
# import items
# API_VERSION = 5
# API_URL     = 'http://localhost:8765'

# class AnkiResource:
# 	def __init__(self):
# 		pass
# 	# sublime.error_message("Could not find a definition")
# 	def makeRequest(self, action, params={}):
# 		# request = json.dumps([ action, params ])
# 		try:
# 			r = requests.post("http://127.0.0.1:8765", json=
# 											{
# 												"action": action,
# 												"version": 5,
# 												"params": params
# 											}
# 						)
# 		except requests.exceptions.ConnectionError:
# 			print('无法连接AnkiConnect端口，请安装该插件后重启Anki')
# 			return {}

# 		else:
# 			print(r.json())
# 			#return a dictionay
# 			print(type(r.json()))
# 			print('已连接Anki，正在处理结果...')
# 			return r.json()

# 	def addNote(self, params):
# 		if params:
# 			return self.makeRequest('addNote', params);

# 	# return all the model name in a dict
# 	def getModelNames(self):
# 		return self.makeRequest('modelNames');

# 	# return a model field in a dict
# 	def getModelFieldNames(self, params):
# # 		params ={ "modelName":'知识点-Mix (Leaflyer)'}
# #		x.getModelFieldNames(params)
# 		return self.makeRequest('modelFieldNames', params);
# 	# Version
# 	def getVersion(self,params):
# 	# return self.makeRequest('version');
# 		return self.makeRequest(params);

# 	def getDeckNames(self):
# 	# return self.makeRequest('version');
# 		return self.makeRequest('deckNames');





class Resource:
	_local_port = 'http://127.0.0.1:8765'
	_version = 5
	def __init__(self, cmd, something=[]):
		# These CMDs are based on the API of AnkiConnect
		# For more detail, see https://foosoft.net/projects/anki-connect/
		self.res = {}
		CMDs ={
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
		if cmd in CMDs:
			action = CMDs[cmd][0]
			params = CMDs[cmd][1]
			self.res = self.make_a_request(action, params)
		else:
			self.res = {}

	def make_a_request(self, action, params):
		res = {}
		try:
			res = requests.post(Resource._local_port,
											json = {
													'action': action,
													'params': params,
													'version': Resource._version
													})
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
		self.fields = self.getFields(name)

	#return fields of a model
	def getFields(self, name):
		dic = Resource(5, name).res
		# print(modelFieldNameDict)
		if 'result' in dic:
			# print(modelNameDict.get('result'))
			li =  dic.get('result')
		return li

class Models:
	def __init__(self):
		self.name_list = self.getModels()
	def getModels(self):
		dic = Resource(3).res
		# print(modelFieldNameDict)
		if 'result' in dic:
			# print(modelNameDict.get('result'))
			li =  dic.get('result')
		return li
class Decks:
	def __init__(self):
		self.name_list = self.getDecks()
	def getDecks(self):
		dic = Resource(4).res
		# print(modelFieldNameDict)
		if 'result' in dic:
			# print(modelNameDict.get('result'))
			li =  dic.get('result')
		return li

class Note:
	def __init__(self, body):
		self.deck        = self.parseDeckName(body)
		self.model       = Model(self.parseModelName(body))
		self.fields_dict = self.parseTXT2Fields(body)
		self.tags_list   = self.parseTags(body)
		self.is_sent 	 = False
		self.id 	     = None
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
		note = {
					'deckName' :self.deck,
					'modelName':self.model.name,
					'fields'   :self.fields_dict,
					'tags'     :self.tags_list
				}

		dic = Resource(6, note).res
		if 'result' in dic:
			id =  dic.get('result')
			self.is_sent = True
			self.id = id
			print(self.id)
			print(self.is_sent)


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
			Note(a_note_str).sendNote()

