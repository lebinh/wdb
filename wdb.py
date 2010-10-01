#!/usr/bin/env python

import urllib2
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup
from WordsDB import WordsDB

DB_FILE = 'words.db'
verbose = False

def clean(lines):
  def format(line):
    # quick and dirty fix for the 'too much spaces in examples' problem
    if line.strip()[0] == '"':
      return "     " + line.strip()
    else:
      return line
  return '\n'.join([format(s) for s in lines.splitlines() if s.strip()])


def get_def(word):
  page = urllib2.urlopen('http://ninjawords.com/%s' % word)
  soup = BeautifulSoup(page)
  if soup.find('p', 'error'): return None
  if soup.find('span','correct-word'): return None
  for marker in soup.findAll('span', 'definition-marker'):
    marker.replaceWith(' - ')
  res = ''
  for dd in soup.findAll('dd'):
    if dd['class'] != 'synonyms':
      defn = ''.join(dd.findAll(text=True))
      res += clean(defn) + '\n'
  return res[:-1] # extract last newline char


def log(msg):
  """print message iff the verbose option is set"""
  if verbose: print msg


def add_to_db(word, dic):
  df = dic.look_up(word)
  if df:
    log('Word "%s" is already in database.' % word)
  else:
    df = get_def(word)
    if df:
      dic.add(word, df)
      log('Word "%s" was added to the database with the following definition:\n%s' % (word, df))
    else:
      print 'Cannot find the definition of "%s". Skipped.' % word


def main():
  usage = 'usage: %prog [options] action [words]\n\n'
  usage += 'Supported actions: list, add, delete\n'
  usage += '  list \t\t list all words in database\n'
  usage += '  add \t\t add words into database\n'
  usage += '  delete \t remove words from database'
  parser= OptionParser(usage)
  parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='verbose output')
  opt, args = parser.parse_args()
  # incorrect numbers of arguments
  if not args:
    parser.print_usage()
    return

  # options handler
  if opt.verbose: 
    global verbose 
    verbose = True

  # actions handler
  action = args[0]
  dic = WordsDB(DB_FILE)
  if action == 'list':
    for word, df in dic.all():
      print '===== %s =====\n%s\n' % (word, df)
    dic.close()
  elif action == 'add':
    for arg in args[1:]:
      add_to_db(arg, dic)
    dic.close()
  elif action == 'delete':
    dic.delete_all(args[1:])
    dic.close()
  else:
    print 'Unknown action: %s' %action
    parser.print_usage()


if __name__ == '__main__':
  main()
