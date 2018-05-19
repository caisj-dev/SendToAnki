import json
import string
import re
# import asyncio
import requests
import  markdown2
import time


# class Command:
# 	VERSION           = ['version',  	    {}]
# 	# MODEL_FIELD_NAMES = ['modelFieldNames', { "modelName": something}]

	# CMDs ={
	# 			1 : ['version',  	    {}],
	# 			2 : ['sync',  			{}],
	# 			3 : ['modelNames',      {}],
	# 			4 : ['deckNames', 	    {}],
	# 			# 'something' should be str type
	# 			5 : ['modelFieldNames', { "modelName": something}],
	# 			##'something' should be dict type
	# 			6 : ['addNote',    	    { "note": something}],
	# 			##'something' should be list type
	# 			7 : ['canAddNotes', 	{ "notes": something}],
	# 			8 : ['updateNoteFields',{ "notes": something}],
	# 	}
# class Resource(Command):
# 	_local_port = 'http://127.0.0.1:8765'
# 	_version = 5
# 	def __init__(self, cmd, something=[]):
# 		# These CMDs are based on the API of AnkiConnect
# 		# For more detail, see https://foosoft.net/projects/anki-connect/
# 		self.res = {}

# 		if cmd in self.VERSION:
# 			action = CMDs[cmd][0]
# 			params = CMDs[cmd][1]
# 			self.res = self.make_a_request(action, params)
# 		else:
# 			self.res = {}

# 	def make_a_request(self, action, params):
# 		res = {}
# 		try:
# 			res = requests.post(Resource._local_port,
# 											json = {
# 													'action': action,
# 													'params': params,
# 													'version': Resource._version
# 													})
# 			res = res.json()
# 		except requests.exceptions.ConnectionError:
# 			print('无法连接AnkiConnect端口')
# 			return res
# 		else:
# 			if len(res) == 2:
# 				print('已连接Anki，正在处理结果...')
# 				return res















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
	def __init__(self, noteBody):
		self.deck        = self.parseDeckName(noteBody)
		self.model       = Model(self.parseModelName(noteBody))
		self.fields_dict = self.parseTXT2Fields(noteBody)
		self.tags_list   = self.parseTags(noteBody)
		self.is_sent 	 = False
		self.id 	     = None
		#TODO:
		#Add new item: record its current position,
		#input: noteBody
		#output: point or region


	# return noteBody of note, dict
	def parseTXT2Fields(self, noteBody):
		d = {}
		#pat =  '##{0}([.\n]+)##{0}|##([.\n]+)---'.format(field,field)
		for field in self.model.fields:
			# st = '##{0}\n([\s\S]+)##'.format(field)
			pat = re.compile(r'{0}'.format('##{0}\n([\s\S]+?)##'.format(field)))

			res = pat.search(noteBody)
			if res != None:
				res = res.group(1)
				d[field] = markdown2.markdown(res, extras=["cuddled-lists"])
			else:
				# the last field
				st = '##{0}\n([\s\S]+?)\n======'.format(field)
				pat = re.compile(r'{0}'.format(st))
				res = pat.search(noteBody)
				if res != None:
					res = res.group(1)
					d[field] = markdown2.markdown(res, extras=["cuddled-lists"])
				else:
					d[field] = ''
		return d
	# return model name from sublime text
	def parseModelName(self, noteBody):
		pat = re.compile(r'{0}'.format('Model:([\s\S]+?)\n'))
		res_model = pat.search(noteBody)
		if res_model != None:
			res_model = res_model.group(1)
		else:
			return ''
		return res_model

	def parseDeckName(self, noteBody):
		pat = re.compile(r'{0}'.format('Deck:([\s\S]+?)\n'))
		res_deck = pat.search(noteBody)
		if res_deck != None:
			res_deck = res_deck.group(1)
		else:
			return ''
		return res_deck

	#TODO： return list of tags
	def parseTags(self, noteBody):
		res_tag = []
		pat = re.compile(r'{0}'.format('##Tags([\s\S]+?)##'))
		res = pat.search(noteBody)
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
		if 'result' in dic and dic.get('result') != None:
			id =  dic.get('result')

			self.is_sent = True
			self.id = id
			# print(self.id)
			# print(self.is_sent)
		elif dic.get('error'):
				print(dic.get('error'))
				# print('duplicated notes number:{0}'.format())
		# Sync
		# time.sleep(1)
		# Resource(2)


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

			noteBody_list = []
			# add Tag
			noteBody_list.append('##Tags')

			for field in self.fields_list:
				noteBody_list.append('##' + field)
			noteBody_list.append('============================\n')
			# seperate by two line, easy to read in MarkDown
			str  = '\n\n'
			note_string = str.join(noteBody_list)

			note_string = info_string + note_string
			print(note_string)
			return note_string
		else:
			return ''

class NoteBook:
	def __init__(self, bookBody):
		self.bookBody = bookBody
		self.num_note_sent = 0
	def send(self):
		pat = re.compile(r'\n===========')
		res_spli = pat.split(self.bookBody)
		leng = len(res_spli )
		# print(leng)
		i = 0
		for a_note_str in res_spli:
			i += 1
			#discard the last item in res_spli
			if i == leng :
				break
			n = Note(a_note_str)
			n.sendNote()
			if n.is_sent:
				self.num_note_sent += 1
				#TODO:
				#add sent syntax to this note in sublime
				#find(pattern, start_point, <flags>)
