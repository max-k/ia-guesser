# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, Sequence, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, Sequence('question_id_seq'), primary_key=True)

    text = Column(String(1024), nullable=False, unique=True)
    yes_count = Column(Integer, nullable=False, default=0)
    no_count = Column(Integer, nullable=False, default=0)

    answers = relationship("Answer", backref="question",
                           cascade="all, delete, delete-orphan")

    def __init__(self, text, yes_count=0, no_count=0):
        self.text = text
        self.yes_count = yes_count
        self.no_count = no_count

    def __repr__(self):
        return("<Question('%s',%s,%s)>" % (self.text,
                                           self.yes_count,
                                           self.no_count))

class Mystery(Base):
    __tablename__ = 'mysteries'

    id = Column(Integer, Sequence('mystery_id_seq'), primary_key=True)

    name = Column(String(50), nullable=False, unique=True)
    stats = Column(Integer, nullable=False, default=0)

    answers = relationship("Answer", backref="mystery",
                           cascade="all, delete, delete-orphan")

    def __init__(self, name, stats=0):
        self.name = name
        self.stats = stats

    def __repr__(self):
        return("<Mystery('%s',%s)>" % (self.text, self.stats))

class Answer(Base):
    __tablename__ = 'answers'
    __table_args__ = (UniqueConstraint('qid', 'mid', name='answer_qid_mid_uc'),)

    qid = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    mid = Column(Integer, ForeignKey('mysteries.id'), primary_key=True)

    answer = Column(Boolean, nullable=False)

    def __init__(self, question_id, mystery_id, answer):
        self.qid = question_id
        self.mid = mystery_id
        self.answer = answer

    def __repr__(self):
        return("<Answer(%s,%s,%s)>" % (self.qid, self.mid, self.answer))

