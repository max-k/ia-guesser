# -*- coding: utf-8 -*-

from model import *
from config import database

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

class Database(object):

    def __init__(self, cnx_string=database, reset=False):
        self.cnx_string = cnx_string
        try:
            self.engine = create_engine(self.cnx_string)
        except Exception as e:
            raise e
        if reset:
            try:
                self._reinit()
            except Exception as e:
                raise e
        try:
            self.cnx = sessionmaker(bind=self.engine)()
        except Exception as e:
            raise e
        if self.engine.driver == 'pysqlite':
            try:
                self._setSqlitePragma()
            except Exception as e:
                raise(e)

    def _reinit(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def _setSqlitePragma(self):
        self.cnx.execute("PRAGMA foreign_keys=ON")
        self.cnx.commit()

    def addQuestion(self, question):
        try:
            q = self.cnx.query(Question).filter(Question.text==question).one()
        except:
            q = Question(question)
            try:
                self.cnx.add(q)
                self.cnx.commit()
                return q
            except Exception as e:
                raise e
        return q

    def addMystery(self, mystery):
        try:
            m = self.cnx.query(Mystery).filter(Mystery.name==mystery).one()
        except:
            m = Mystery(mystery)
            try:
                self.cnx.add(m)
                self.cnx.commit()
                return m
            except Exception as e:
                raise e
        return m

    def addAnswer(self, question, mystery, answer=None):
        q = question
        if isinstance(Question, question):
            q = question.id
        m = mystery
        if isinstance(Mystery, mystery):
            m = mystery.id
        try:
            a = self.cnx.query(Answer).filter(and_(qid==q,mid=m)).one()
        except:
            a = Answer(q, m, answer)
            try:
                self.cnx.add(a)
                self.cnx.commit()
                return a
            except Exception as e:
                raise e
        return a

