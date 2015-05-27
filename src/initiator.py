# -*- coding: utf-8 -*-

from lib.words import Word
from lib.modules import checkModule

if checkModule("cPickle"):
    from cPickle import load, dump, HIGHEST_PROTOCOL
else:
    from pickle import load, dump, HIGHEST_PROTOCOL

import sys
from os.path import join, isfile

class Initiator(object):

    def __init__(self, qpath="data/src", wpath="data"):
        self.wpath = wpath
        self.qfile = join(qpath, "questions.txt")
        self.ofile = join(qpath, "objets.txt")
        try:
            qhandler = open(self.qfile, 'r')
        except Exception as e:
            print(self.qfile)
            print(e)
            sys.exit(1)
        try:
            ohandler = open(self.ofile, 'r')
        except Exception as e:
            printf(self.ofile)
            print(e)
            sys.exit(1)
        self.questions = sorted(q[:-1] for q in qhandler.readlines())
        self.objects = sorted(o[:-1] for o in ohandler.readlines())
        qhandler.close()
        ohandler.close()

class Asker(Initiator):

    def __init__(self, qpath="data/src", wpath="data"):
        super(Asker, self).__init__(qpath, wpath)

    def run(self):
        for name in self.objects:
            wobject = Word(name, self.wpath)
            if self.questions == wobject.questions:
                continue
            print("questions : {}".format(wobject.questions))
            for question in wobject.questions:
                if question not in self.questions:
                    del wobject.data["answers"][question]
            for question in self.questions:
                if question not in wobject.questions:
                    wobject.update(question)

class WordManager(Initiator):

    def __init__(self, words, qpath="data/src", wpath="data"):
        super(WordManager, self).__init__(qpath, wpath)
        self.words = words
        for word in self.words:
            if word not in self.objects:
                print("Le mot `{}` n'existe pas".format(word))
                sys.exit(1)

class Updater(WordManager):

    def run(self):
        another = True
        while another:
            question = input("Veuillez saisir une question à mettre à jour :")
            if question not in self.questions:
                print("La question saisie n'existe pas")
            else:
                for w in self.words:
                    word = Word(w, self.wpath)
                    word.update(question)
            another = None
            print("Voulez-vous mettre à jour une autre question ? [o/n]")
            while another == None:
                ch = sys.stdin.read(1)
                if ch in ['y', 'Y', 'o', 'O']:
                    another = True
                if ch in ['n', 'N']:
                    another = False

class Printer(WordManager):

    def run(self):
        for w in self.words:
            if not isfile(join(self.wpath, "{}.bindata".format(w))):
                print("Fichier {} non défini".format(w))
                continue
            word = Word(w, self.wpath)
            for question in self.questions:
                word.print(question)
            print("")

