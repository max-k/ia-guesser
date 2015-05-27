# -*- coding: utf-8 -*-

from lib.modules import checkModule

if checkModule("cPickle"):
    from cPickle import load, dump, HIGHEST_PROTOCOL
else:
    from pickle import load, dump, HIGHEST_PROTOCOL

from os.path import join

class Word(object):

    def __init__(self, name, path):
        self.data = {}
        self.name = name
        self.file = join(path, "{}.bindata".format(self.name))
        self._read()

    def _read(self):
        try:
            handler = open(self.file, 'rb')
            try:
                self.data = load(handler)
            except:
                self.data = {"answers": {}}
            handler.close()
        except:
            self.data = {"answers": {}}
        finally:
            self.questions = sorted(self.data["answers"].keys())

    def _write(self):
        try:
            handler = open(self.file, 'wb')
        except Exception as e:
            raise e
        try:
            dump(self.data, handler, HIGHEST_PROTOCOL)
            handler.close()
        except Exception as e:
            handler.close()
            raise e

    def update(self, question):
        answer = None
        print("{} : {} ? [o/n]".format(self.name, question))
        while answer == None:
            ch = sys.stdin.read(1)
            if ch in ['y', 'Y', 'o', 'O']:
                answer = True
            if ch in ['n', 'N']:
                answer = False
        self.data["answers"][question] = answer
        self._write()

    def print(self, question):
        answer = None
        if question in self.data["answers"]:
            answer = self.data["answers"][question]
        print("[{}] {} : {}".format(self.name, question, answer))

