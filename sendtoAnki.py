#TechSideOnline.com Webify Sublime Text 3 plugin example
from .AnkiResource import AnkiResource,Note,MyHelper,ForTest
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
	deckList = []
	deck = ''
	model = ''
	def run(self, edit):
		# this will populate the quick_panel with models of markdown formats
		# self.list = self.getParsedModel()
		self.deckList = MyHelper.parseDeckName2List()
		#show  the above list in the panel,
		#self.on_done is called when one  of the item was chosen by user
		self.view.window().show_quick_panel(self.deckList, self.on_done,1, 0)
		# MyHelper.parseMDCardInfo('model:dab')
		# decksLst =
		# for deck in decksLst:
		# 	print(deck)

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
		self.view.window().show_quick_panel(self.modelList, self.on_done_chose_model,1, 0)

	def on_done_chose_model(self, index):
		if index ==  -1:
			return
		# if user picks from list, return the correct entry
		self.view.run_command(
		"insert_my_text", {
		"args":
			{'text': self.modelList[index][1]}
		})

	#get a list of model from  anki, each of them  are parsed into Markdown
	def getParsedModel(self):
		parsedModel =[]
		#get all model names in list
		modelList = MyHelper.parseModelName2List()
		deck = self.deck
		#parse each of the model in the list
		for model in modelList:
			parsedModel.append([model,Note.cardModel2MarkdowndSyntax(model, deck)])
		return parsedModel

class InsertMyText(sublime_plugin.TextCommand):
	 def run(self, edit, args):
	 	self.view.insert(edit, self.view.sel()[0].begin(), args['text'])


class SendToAnkiCommand(sublime_plugin.TextCommand): #create Webify Text Command
	def run(self, edit):   #implement run method
		x = AnkiResource()
		# print (ForTest.ModelNameList ())
		ForTest.ModelNameList ()

		print(x.getDeckNames())
		deckName = 'Programing&Algorithm'
		ModelName = '知识点-Basic (Leaflyer)'
		tags = ['InnerClass']
		for region in self.view.sel():  #get user selection
			if not region.empty():  #if selection not empty then
				s = self.view.substr(region)  #assign s variable the selected region
				# print(s)
				linesList = s.splitlines()
				notes = self.getNotes(linesList)
				for k, v in notes.items():
					print(k, v)
					v = markdown2.markdown(v, extras=["cuddled-lists"])  # or use `html = markdown_path(PATH)`
					k = markdown2.markdown(k, extras=["cuddled-lists"])  # or use `html = markdown_path(PATH)`
					# print( markdown2.markdown('Use the `printf()` function.') )

					Note.add(deckName, ModelName, k, v,tags )
				# self.view.replace(edit, region, news) #replace content in view
				a = 'I did these things:\n* bullet1\n* bullet2\n* bullet3\n'
				print(markdown2.markdown(a, extras=["cuddled-lists"]))
			else:
				print('空的region')


	def getNotes(self, listOfLines):
		"""
		A note includes Question field and Answer field.
		For list of lines, which includes many notes.
		each note may has multiple Question lines,
		and the vary first one starts with Syntax '#',
		followed by Answer lines, whose vary first line
		starts with'##'

		retun a dictionry:
			Key:Question
			Value: Answer

		"""
		p = 0
		i = 0
		notesDict = dict()
		while p < len(listOfLines):
			s = ''
			questionList = []
			answerList = []
			# if not MyHelper.isQusetionSyntax(listOfLines[p]):
			# 	p += 1
			# 	continue

			print(i)
			if MyHelper.isQusetionSyntax(listOfLines[i]):
				i = p
				while not MyHelper.isAnswerSyntax(listOfLines[i]):
					#ignore the Syntax line
					if MyHelper.isQusetionSyntax(listOfLines[i]):
						i += 1
						continue
					print('Entering Question text')
					questionList.append( listOfLines[i] )
					questionList.append( '\n')
					i += 1
				# get one note's Question
				questionString = s.join(questionList)
				print(questionString)
			while not MyHelper.isQusetionSyntax(listOfLines[i]):
				#ignore the Syntax line
				if MyHelper.isAnswerSyntax(listOfLines[i]):
					i += 1
					continue
				print('Entering answer text')
				answerList.append( listOfLines[i] )
				answerList.append( '\n')
				i += 1
				if (i >= len(listOfLines)):
					break
			answerString = s.join(answerList)
			print(answerString)
			notesDict[questionString] = answerString
			p = i
			# p = p + 1
		print('EddND')
		return notesDict




class TestCommand(sublime_plugin.TextCommand):  #Test command
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				s = self.view.substr(region)
				news = s.replace('&lt;', '<')  #reversed from Webify
				news = news.replace('&gt;', '>')  #reversed from Webify
				self.view.replace(edit, region, news)
