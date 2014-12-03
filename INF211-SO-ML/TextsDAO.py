import nltk
from html.parser import HTMLParser


# Implementation specific imports
from os import listdir
from os.path import isfile, join 
import codecs

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
    def __init__(self, base_dir):
        self.__base_dir = base_dir

    def __iter__(self):
        files = [f for f in listdir(self.__base_dir) if isfile(join(self.__base_dir, f))]
        for f in files:
            post = self.extract(f)
            yield self.tokenize(post)
    
    def extract(self, file_name):
        with codecs.open(join(self.__base_dir, file_name), "r", "utf-8") as file:
            return file.readlines()[2]

    def tokenize(self, string):
        """logic to tokenize a string. Involves removing tags, splitting, lowercasing words etc"""
        s = MLStripper()
        s.feed(string)
        string = ''.join(e for e in s.get_data() if e.isalnum() or e == ' ')
        return string.lower().split()