#TechSideOnline.com Webify Sublime Text 3 plugin example
from .AnkiResource import AnkiResource,Note,MyHelper,ForTest,Model,Notes,Template,NoteBook,Resource
# from .Markdown2 import Markdown
# import urllib
import requests
import datetime
# from requests import Request
import sublime
import sublime_plugin
import re, string  #import the required modules
import json
import jinja2
import markdown2

class InsertNoteFieldBySyntaxCommand(sublime_plugin.TextCommand):
	# deckList = []
	# deck = ''
	# model = ''
	def run(self, edit):
		# this will populate the quick_panel with models of markdown formats
		# self.list = self.getParsedModel()
		self.deckList = MyHelper.parseDeckName2List()

		#show  the above list in the panel,
		#self.on_done is called when one  of the item was chosen by user
		self.view.window().show_quick_panel(self.deckList, self.on_done,1, 0)

	def on_done(self, index):
		#  if user cancels with Esc key, do nothing
		#  if canceled, index is returned as  -1
		if index == -1:
			return
		# if user picks from list, #save the deck name for now
		self.deck = self.deckList[index]
		#get model list from anki in MD format
		self.modelList = self.getParsedModel()
		# show modellist panel
		self.view.window().show_quick_panel(self.modelList, self.on_done_chose_model,1, 3)

	def on_done_chose_model(self, index):
		if index ==  -1:
			return
		# if user picks from list, return the correct entry
		self.view.run_command(
		"insert_my_text", {
		"args":
			{'text': self.modelList[index][1]}
		})
		# self.view.run_command(
		# "move_cursor",{})





	#get a list of model from  anki, each of them  are parsed into Markdown
	def getParsedModel(self):
		parsedModel =[]
		#get all model names in list
		modelList = MyHelper.parseModelName2List()
		deck = self.deck
		#parse each of the model in the list
		for model in modelList:
			parsedModel.append([model,Template(deck, model).new()])
		return parsedModel



class InsertMyText(sublime_plugin.TextCommand):
	 def run(self, edit, args):
	 	line = 1
	 	#move the cursor to the begin of document, personal preference
	 	point = self.view.text_point(line - 1, 0)
	 	self.view.insert(edit, point, args['text'])

class MoveCursorCommand(sublime_plugin.TextCommand):
	 def run(self, edit, args):
	 	line = 5
	 	#move the cursor to the begin of document, personal preference
	 	point = self.view.text_point(line - 1, 0)
	 	self.view.insert(edit, point,'')


class SendToAnkiCommand(sublime_plugin.TextCommand): #create Webify Text Command
	def run(self, edit):   #implement run method
		for region in self.view.sel():  #get user selection
			if not region.empty():  #if selection not empty then
				sel_str = self.view.substr(region)  #assign s variable the selected region
				notes = NoteBook(sel_str)
				notes.send()
				sublime.status_message('ok')
		# res = Resource('5','知识点-Mix (Leaflyer)').res
		# print(type(res))
		# print(res['result'])
		print(Model('知识点-Mix (Leaflyer)').fields)


	# def getNotes(self, listOfLines):

	# 	p = 0
	# 	i = 0
	# 	notesDict = dict()
	# 	while p < len(listOfLines):
	# 		s = ''
	# 		questionList = []
	# 		answerList = []
	# 		# if not MyHelper.isQusetionSyntax(listOfLines[p]):
	# 		# 	p += 1
	# 		# 	continue

	# 		print(i)
	# 		if MyHelper.isQusetionSyntax(listOfLines[i]):
	# 			i = p
	# 			while not MyHelper.isAnswerSyntax(listOfLines[i]):
	# 				#ignore the Syntax line
	# 				if MyHelper.isQusetionSyntax(listOfLines[i]):
	# 					i += 1
	# 					continue
	# 				print('Entering Question text')
	# 				questionList.append( listOfLines[i] )
	# 				questionList.append( '\n')
	# 				i += 1
	# 			# get one note's Question
	# 			questionString = s.join(questionList)
	# 			print(questionString)
	# 		while not MyHelper.isQusetionSyntax(listOfLines[i]):
	# 			#ignore the Syntax line
	# 			if MyHelper.isAnswerSyntax(listOfLines[i]):
	# 				i += 1
	# 				continue
	# 			print('Entering answer text')
	# 			answerList.append( listOfLines[i] )
	# 			answerList.append( '\n')
	# 			i += 1
	# 			if (i >= len(listOfLines)):
	# 				break
	# 		answerString = s.join(answerList)
	# 		print(answerString)
	# 		notesDict[questionString] = answerString
	# 		p = i
	# 		# p = p + 1
	# 	print('EddND')
	# 	return notesDict



