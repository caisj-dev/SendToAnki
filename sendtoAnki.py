
from .AnkiResource import Note,Model,Decks,Template,Resource

import requests
import datetime

import sublime
import sublime_plugin
import re, string  #import the required modules
import json

import time

class NewNoteCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # this will populate the quick_panel with models of markdown formats
        # self.list = self.model_name()
        self.deck_list = Decks().name_list

        #show  the above list in the panel,
        #self.on_done is called when one of the item was chosen by user
        if self.deck_list is not None:
            self.view.window().show_quick_panel(self.deck_list, self.on_done_chosing_deck, 1, 0)

    def on_done_chosing_deck(self, index):
        #  if user cancels with Esc key, do nothing
        #  if canceled, index is returned as  -1
        if index == -1:
            return
        # if user picks from list, #save the deck name for now
        self.deck = self.deck_list[index]
        #get model list from anki in MD format
        self.model_list = [ [model, Template(self.deck, model).new()] for model in Model().all_models_list()]
        # show model_list panel
        self.view.window().show_quick_panel(self.model_list, self.on_done_chose_model,1, 0)

    def on_done_chose_model(self, index):
        if index ==  -1:
            return
        # if user picks from list, return the correct entry

        line = 1
        #move the cursor to the begin of document, personal preference
        self.view.run_command(
        "insert_my_text", {
        "args":
            {'text': self.model_list[index][1]}
        })



class InsertMyText(sublime_plugin.TextCommand):
     def run(self, edit, args):
        line = 1
        #move the cursor to the begin of document, personal preference
        point = self.view.text_point(line - 1, 0)
        self.view.insert(edit, point, args['text'])
        self.view.show(point)

class MoveCursorCommand(sublime_plugin.TextCommand):
     def run(self, edit, args):
        line = 5
        #move the cursor to the begin of document, personal preference
        point = self.view.text_point(line - 1, 0)
        # self.view.insert(edit, point,'')

class SendToAnkiCommand(sublime_plugin.TextCommand): #create Webify Text Command
    def run(self, edit):   #implement run method
        '''Two strategies are defined to send notes:
                1. notes that are going to be sent for the first time,
                whose state is '☐', would be sent for sure.
                2. notes that are sent, whose state is '✔', would be ignore.
        '''
        suc_num = 0
        sp = 0
        note_rg = self.find_one_note_region_from(sp)
        while note_rg != None:
            n = Note(self.view, edit, note_rg)
            # those already exit in Anki will be ignored
            if ('✔' in n.state):
                print('ignore it')
                sp = sp + n.rg_size
                note_rg = self.find_one_note_region_from(sp)
                # self.view.fold(note_rg)
                continue
            n.send_it()
            suc_num += 1
            # if self.view.fold(note_rg):
            #     print('fold note!')
            sp = sp + n.rg_size
            # print(sp)
            note_rg = self.find_one_note_region_from(sp)
            time.sleep(0.01)

        sublime.ok_cancel_dialog('已添加{0}条笔记，马上同步至AnkiWeb吗?'.format(suc_num), '同步')

    def is_empty_match(self, match):
        return match.size() == 0

    def find_all_notes(self):
        ''' this method return all the notes' region in a list

        '''
        s = 'Deck:([\s\S]+?)\n===='
        match_region = self.view.find_all(r'{0}'.format(s),0)

    def find_one_note_region_from(self, start_point):
        ''' this method return one note's region

        '''
        s = 'Deck :([\s\S]+?)\n===='
        one_note_region = self.view.find(r'{0}'.format(s), start_point)

        find_no_note = self.is_empty_match(one_note_region)
        if find_no_note :
            print('no note left!')
            return None
        else:
            return one_note_region


