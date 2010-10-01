#!/usr/bin/env python

import os
import sqlite3

CREATE_TABLE = '''create table words (word text, definition text)'''
LOOK_UP_WORD = '''select * from words where word=?'''
ADD_WORD = '''insert or ignore into words values (?, ?)'''
ALL_WORDS = '''select * from words'''
DEL_WORD = '''delete from words where word=?'''

class WordsDB:
  def __init__(self, data_file):
    self.filename = data_file
    self.is_open = False

  def check_db_ready(self):
    if not self.is_open:
      self.con = self.load_db()

  def load_db(self):
    """load words data from file"""
    if not os.path.exists(self.filename):
      con = sqlite3.connect(self.filename)
      con.execute(CREATE_TABLE)
    else:
      con = sqlite3.connect(self.filename)
    self.is_open = True
    return con

  def look_up(self, word):
    self.check_db_ready()
    res = self.con.execute(LOOK_UP_WORD, (word,)).fetchone()
    if res:
      return res[1]
    else:
      return None

  def add(self, word, definition):
    self.check_db_ready()
    self.con.execute(ADD_WORD, (word, definition))

  def delete(self, word):
    self.check_db_ready()
    self.con.execute(DEL_WORD, (word,))

  def delete_all(self, words):
    self.check_db_ready()
    for word in words:
      self.con.execute(DEL_WORD, (word,))

  def close(self):
    if self.is_open:
      self.con.commit()
      self.con.close()
      self.is_open = False

  def all(self):
    self.check_db_ready()
    return self.con.execute(ALL_WORDS).fetchall()

