import os
import sys
import json
import string
import re

import requests

abspath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abspath)
import markdown2


import time

import sublime, sublime_plugin

class Resource:
    _local_port = 'http://127.0.0.1:8765'
    _version = 5
    def __init__(self, cmd, something=[]):
        # These CMDs are based on the API of AnkiConnect
        # For more detail, see https://foosoft.net/projects/anki-connect/
        self.res = {}
        CMDs ={
                1 : ['version',         {}],
                2 : ['sync',            {}],
                3 : ['modelNames',      {}],
                4 : ['deckNames',       {}],
                # 'something' should be str type
                5 : ['modelFieldNames', { "modelName": something}],
                ##'something' should be dict type
                6 : ['addNote',         { "note": something}],
                ##'something' should be list type
                7 : ['canAddNotes',     { "notes": something}],
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
            print('Unable to connect to AnkiConnect port, please check that Anki plugin')
            sublime.error_message('Unable to connect to AnkiConnect port, please check that Anki plugin')
            return res
        else:
            if len(res) == 2:
                print('Successful connection to Anki，processing ...')
                return res

class Model:
    def __init__(self, name=None):
        self.name = name
    def get_fields_list(self):
        li = []
        dic = Resource(5, self.name).res
        if 'result' in dic:
            li =  dic.get('result')
        return li

    def all_models_list(self):
        li = []
        dic = Resource(3).res
        if 'result' in dic:
            li =  dic.get('result')
        return li



class Decks:
    def __init__(self):
        self.name_list = self.getDecks()
    def getDecks(self):
        li = []
        dic = Resource(4).res
        # print(modelFieldNameDict)
        if 'result' in dic:
            # print(modelNameDict.get('result'))
            li =  dic.get('result')
        return li

class Note:
    def __init__(self, view, edit, region):
        # rg_start_line,rg_end_line are both region type

        self.region = region
        self.rg_size = region.size()
        self.view =  view
        self.edit = edit
        self.note_body   = self.get_note_body(view, region)
        self.deck        = self.parse_deck_name(self.note_body)
        self.model       = Model(self.parse_model_name(self.note_body))
        self.fields_dict = self.parse_note_fields(self.note_body)
        self.tags_list   = self.parse_tags(self.note_body)
        self.state       = self.parse_state()
        self.is_sent     = False
        self.id          = None

        #TODO:
        #Add new item: record its current position,
        #input: noteBody
        #output: point or region

    def is_empty_match(self, match):
        return match is None

    def get_note_body(self, view, region):
        ''' return note string
        '''
        return view.substr(region)

    def rg_state_line(self):
        '''return a the state region in the view
        '''
        s = 'State([\s\S]+?)\n'
        state_rg = self.view.find(r'{0}'.format(s), self.region.begin())
        # state_rg = self.view.line(state_rg)
        return state_rg

    # return body of note in a dict
    def parse_note_fields(self, note_body):
        d = {}
        #pat =  '##{0}([.\n]+)##{0}|##([.\n]+)---'.format(field,field)
        for field in self.model.get_fields_list():
            # st = '##{0}\n([\s\S]+)##'.format(field)
            pat = re.compile(r'{0}'.format('##{0}\n([\s\S]+?)##'.format(field)))

            res = pat.search(note_body)
            if res != None:
                res = res.group(1)
                d[field] = markdown2.markdown(res, extras=["cuddled-lists"])
            else:
                # the last field
                st = '##{0}\n([\s\S]+?)\n======'.format(field)
                pat = re.compile(r'{0}'.format(st))
                res = pat.search(note_body)
                if res != None:
                    res = res.group(1)
                    d[field] = markdown2.markdown(res, extras=["cuddled-lists"])
                else:
                    d[field] = ''
        return d
    # return model name from sublime text
    def parse_model_name(self, noteBody):
        pat = re.compile(r'{0}'.format('Model:([\s\S]+?)\n'))
        res_model = pat.search(noteBody)
        if res_model != None:
            res_model = res_model.group(1)
        else:
            return ''
        return res_model

    def parse_deck_name(self, noteBody):
        res_deck = ''
        pat = re.compile(r'{0}'.format('Deck :([\s\S]+?)\n'))
        res_match = pat.search(noteBody)
        if res_match != None:
            res_deck = res_match.group(1)
        return res_deck

    def parse_state(self):
        ''' return a note state string, by parsing from view.
        '''
        res_state = ''
        pat = re.compile(r'{0}'.format('State:([\s\S]+?)\n'))
        res_match = pat.search(self.note_body)
        if res_match != None:
            res_state = res_match.group(1)
        return res_state

    def parse_tags(self, noteBody):
        res_tag = []
        pat = re.compile(r'{0}'.format('##Tags([\s\S]+?)##'))
        res = pat.search(noteBody)
        if res != None:
            pat = re.compile(r',')
            res_spli = pat.split(res.group(1))
            res_tag = res_spli
        return res_tag

    def change_state_ok(self):
        ''' action to change the state of note in view
        '''

        state_region = self.rg_state_line()
        # print('important:')
        # print(self.view.substr(state_region))
        self.view.replace(self.edit, state_region, 'State:' + u'✔' + '\n')
        self.state = u'✔'
        # self.view.insert(self.edit, self.rg_start_line.b, u'✔')

    def change_state_fail(self):
        ''' action to change the state of note in view
        '''

        state_region = self.rg_state_line()

        self.view.replace(self.edit, state_region, 'State:'+ u'✘'+ '\n')
        self.state = u'✘'

    def send_it(self):
        '''

        '''
        note = {
                'deckName' :self.deck,
                'modelName':self.model.name,
                'fields'   :self.fields_dict,
                'tags'     :self.tags_list
                }

        dic = Resource(6, note).res
        if (dic.get('result') is None) and ('existing' in dic.get('error')):
            self.is_sent = True
            print('Found one Duplicated note.')
            self.change_state_ok()
            print('Changed state into ok')
        if (dic.get('error') is None ) and (dic.get('result') != None):
            self.id = dic.get('result')
            print(self.id)
            self.change_state_ok()
            # print(dic.get('result'))
            print('Changed state into ok')

        # Sync
        # time.sleep(1)
        # Resource(2)
        print('self.state:{0}'.format(self.state))

#creat new Template by the givin model and deck.
class Template:
    def __init__(self, deck, model):
        self.deck        = deck
        self.model       = model
        self.fields_list = Model(model).get_fields_list()
    #return a template string.
    def new(self):
        # fields_list = self.model.fields
        print(len(self.fields_list))
        if len(self.fields_list) != 0:
            info_list = []
            info_list.append('Deck :'+ self.deck)
            info_list.append('Model:'+ self.model)
            info_list.append('State:'+ u'☐')
            info_list.append('----------------------------\n')
            str  = '\n'
            info_string = str.join(info_list)

            note_body_list = []
            # add Tag
            note_body_list.append('##Tags')

            for field in self.fields_list:
                note_body_list.append('##' + field)
            note_body_list.append('============================\n')
            # seperate by two line, easy to read in MarkDown
            str  = '\n\n'
            note_string = str.join(note_body_list)

            note_string = info_string + note_string
            print(note_string)
            return note_string
        else:
            return ''

# class NoteBook:
#     def __init__(self, view, regions_list):
#         # self.bookBody = self.get_notebook_body()
#         self.note_regions_list = regions_list
#         self.num_notes_sent = 0

#     def send(self):
#         # pat = re.compile(r'\n===========')
#         # res_spli = pat.split(self.bookBody)
#         note_num = len(self.note_regions_list )
#         # print(leng)
#         i = 0
#         for each_note_rg in self.note_regions_list:
#             i += 1
#             #discard the last item in res_spli
#             if i == note_num :
#                 break
#             n = Note(each_note_rg)
#             n.send_it()
#             if n.is_sent:
#                 self.num_notes_sent += 1
#                 #TODO:
#                 #add sent syntax to this note in sublime
#                 #find(pattern, start_point, <flags>)

