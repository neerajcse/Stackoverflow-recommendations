import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

from TextsDAO import TextsDAO
from CorpusDAO import DictionaryDAO
from CorpusDAO import CorpusDAO



BASE_DIR = "H:\Stackoverflow Database\MLData\\"
BASE_META_DIR = "H:\Stackoverflow Database\MLMetaData\\"

def main():
    corpus = CorpusDAO(BASE_META_DIR, BASE_DIR)  
    #for key, value in corpus.getDictionary().items():
    #    print("Key:{} Value:{}".format(key, value))
    for vector in corpus:
        print(vector)

if __name__ == "__main__":
    main()