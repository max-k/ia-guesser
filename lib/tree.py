# -*- coding: utf-8 -*-

class Node(object):

    def __init__(self, question, stats={'yes': 0, 'no': 0}, no=None, yes=None):
        self.question = question
        self.stats = stats
        self.yes = yes
        self.no = no

    def __repr__(self):
        yes = '?'
        no = '?'
        if (self.yes != None and isinstance(self.yes, Leaf)):
            yes = self.yes.words
        if (self.no != None and isinstance(self.no, Leaf)):
            no = self.no.words
        return("<Node('%s',%s,%s,%s)>" % (self.question,
                                          self.stats,
                                          yes,
                                          no))

    def answer(self, answer=None):
        if answer == None:
            return (self.stats['yes'] > self.stats['no'])
        if answer:
            return self.yes
        else:
            return self.no

class Leaf(object):

    def __init__(self, words=None):
        self.words = {}
        if words != None:
            self.words = words

    def __repr__(self):
        return("<Leaf(%s)>" % (self.words))

    def addWord(self, word):
        if word not in self.words:
            self.words[word] = 0

