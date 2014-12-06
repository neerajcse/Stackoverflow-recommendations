from html.parser import HTMLParser
import sqlite3
import time


# Implementation specific imports
from os import listdir
from os.path import isfile, join 
import codecs
import re

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

DEBUG = False

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class TextsDAO(object):
    """Provides an interface to iterate over the corpus of 
    files, returns the text with all stopwords removed."""
    def __init__(self, base_dir, db):
        self.__base_dir = base_dir
        self.__db_name = db

    def __iter__(self):
        """files = [f for f in listdir(self.__base_dir) if isfile(join(self.__base_dir, f))]
        for f in files:
            post = self.extract(f)
            yield self.tokenize(post)
        """
        if DEBUG:
            for doc in documents:
                print("..")
                yield doc.split()
        else:
            self.conn = sqlite3.connect(self.__db_name)
            self.cursor = self.conn.cursor()
            for sid,tags,title,question in self.cursor.execute("select * from posts"):
                print("..")
                yield self.tokenize(title.decode("utf-8") + " " + question.decode("utf-8"))

    def close(self):
        self.conn.close()

    def extract(self, file_name):
        with codecs.open(join(self.__base_dir, file_name), "r", "utf-8") as file:
            return file.readlines()[2]

    def tokenize(self, string):
        """logic to tokenize a string. Involves removing tags, splitting, lowercasing words etc"""
        s = MLStripper()
        s.feed(string)
        new_s = ' '.join([x for x in re.sub('[^a-zA-Z0-9\n\.]', ' ', s.get_data()).split() if len(x) > 1])
        return ' '.join(new_s.split("\n")).split()