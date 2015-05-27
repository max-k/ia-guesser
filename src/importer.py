# -*- coding: utf-8 -*-

from config import database
from lib.words import Word
from lib.database import Database
from src.initiator import Initiator

import sys
from os import getcwd, listdir
from os.path import join, isfile, splitext

class Importer(Initiator):

    def __init__(self, qpath="data/src", wpath="data", cnx_string=database):
        super(Importer, self).__init__(qpath, wpath)
        self.cnx_string = cnx_string
        self.files = (f for f in listdir(join(getcwd(), wpath))
                        if isfile(join(getcwd(), f))
                        and splitext(f)[1] == ".bindata")
        try:
            self.database = Database(cnx_string, reset=True)
        except Exception as e:
            print(e)
            print("Unable to connect to database `{}`".format(self.cnx_string))
            sys.exit(1)

    def run(self):
        qids = {}
        for q in self.questions:
            try:
                qids[q] = self.database.addQuestion(q).id
            except Exception as e:
                print(e)
                print("Unable to persist question `{}` to database".format(q))
                sys.exit(1)
        oids = {}
        for o in self.objects:
            try:
                oids[o] = self.database.addMystery(o).id
            except Exception as e:
                print(e)
                print("Unable to persist object `{}` to database".format(o))
                sys.exit(1)
        for f in self.files:
            name = splitext(f)[0]
            word = Word(name, wpath)
            oid = oids[name]
            for q in word.questions:
                if q in self.questions:
                    answer = word.data["answers"][question]
                    qid = qids[question]
                    try:
                        self.database.addAnswer(qid, oid, answer)
                    except Exception as e:
                        print(e)
                        print("Unable to persist answer to database : ")
                        print("[{}] {} : {}".format(name, question, answer))
                        sys.exit(1)

