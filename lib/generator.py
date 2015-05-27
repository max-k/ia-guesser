# -*- coding: utf-8 -*-

from model import Question, Mystery, Answer
from lib.tree import Node, Leaf
from config import database

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Generator(object):

    def __init__(self, cnx_string=database):
        self.cnx_string = cnx_string
        try:
            self.engine = create_engine(self.cnx_string)
        except Exception as e:
            self.engine = None

    

