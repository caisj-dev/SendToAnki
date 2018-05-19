#TechSideOnline.com Webify Sublime Text 3 plugin example
from .AnkiResource import Note,Model,Models,Decks,Template,NoteBook,Resource
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
        self.deckList = Decks().name_list

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
        # modelList = MyHelper.parseModelName2List()
        modelList = Models().name_list
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
                print('note sent successful:{0}'.format(notes.num_note_sent))
                sublime.status_message('ok')

        # st = '##Question\n([\s\S]+?)##'
        self.find_one_note(edit)
        # # match = self.view.find_all(r'#', 0)
        # match = self.view.find(r'#', 0)
        # find_no_note = self.is_empty_match(match)
        # print('debuging.')
        # if find_no_note:

        #     print('no notes!')
        # else:
        #     # self.view.sel().add_all(match)
        #     self.view.sel().add(match)
        # # rgs = self.view.find_by_selector('markup.heading')
        # # self.view.sel().add_all(rgs)
        # # for rg in rgs:
        # # self.view.insert(edit, rg.b, 'YES')

    def is_empty_match(self, match):
        return match is None

    def find_all_notes(self):
        ''' this method return all the notes' region in a list

        '''
        s = 'Deck:([\s\S]+?)\n===='
        match_region = self.view.find_all(r'{0}'.format(s),0)

    def find_one_note(self,edit):
        ''' this method return one note's region

        '''
        s = 'Deck:([\s\S]+?)\n===='
        match_region = self.view.find(r'{0}'.format(s),0)

        find_no_note = self.is_empty_match(match_region)
        if find_no_note:

            print('no notes!')
        else:
            # test
            # self.view.sel().add(match_region)

            # Returns the line that contains the point.
            # the return type is Region
            # print('region\'s start with:{0}'.format(match_region.begin()))
            # print('region\'s end with:{0}'.format(match_region.end()))
            rg_start_line = self.view.line(match_region.a)

            self.view.insert(edit, rg_start_line.b, 'OK')
            print(self.view.substr(match_region))

            # rg_end_line = self.view.line(match_region.b)
            # print('region\'s first line start with:{0}'.format(rg_start_line.a))
            # print('region\'s first line end with  :{0}'.format(rg_start_line.b))

            # print('region\'s last line start with:{0}'.format(rg_end_line.a))
            # print('region\'s last line end with  :{0}'.format(rg_end_line.b))

            # print(match_region.size())
