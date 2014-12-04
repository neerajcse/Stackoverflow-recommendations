import os
import logging
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

from TextsDAO import TextsDAO
from CorpusDAO import DictionaryDAO
from CorpusDAO import CorpusDAO
from html.parser import HTMLParser

DB = "stackoverflow-posts.db"
BASE_DIR = "."
BASE_META_DIR = "."
SERIALIZED_CORPUS = os.path.join(BASE_META_DIR, "corpus.mm")
SERIALIZED_TFIDF = os.path.join(BASE_META_DIR, "tfidf.model")
SERIALIZED_TFIDF_CORPUS = os.path.join(BASE_META_DIR, "corpus_tfidf.mm")

SERIALIZED_LSI_CORPUS = os.path.join(BASE_META_DIR, "corpus_lsi.mm")
TOPICS_LIST = os.path.join(BASE_META_DIR, "list_topics.list")
SIMILARITY_INDEX = os.path.join(BASE_META_DIR, "similarity.index")

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

def tokenize(string):
        """logic to tokenize a string. Involves removing tags, splitting, lowercasing words etc"""
        s = MLStripper()
        s.feed(string)
        new_s = ' '.join([x for x in re.sub('[^a-zA-Z0-9\n\.]', ' ', s.get_data()).split() if len(x) > 1])
        return ' '.join(new_s.split("\n")).split()

def main():
    dictionary = DictionaryDAO(BASE_META_DIR, BASE_DIR, DB).getDictionary()
    
    if os.path.isfile(SERIALIZED_CORPUS):
        corpus = corpora.MmCorpus(SERIALIZED_CORPUS)
    else:
        corpus_dao = CorpusDAO(BASE_META_DIR, BASE_DIR,DB)
        corpora.MmCorpus.serialize(SERIALIZED_CORPUS, corpus_dao)
        corpus = corpora.MmCorpus(SERIALIZED_CORPUS)

    # Confirm if its populated
    print(len(corpus))

    if os.path.isfile(SERIALIZED_TFIDF):
        tfidf = models.TfidfModel.load(SERIALIZED_TFIDF)
    else:
        tfidf = models.TfidfModel(corpus)
        tfidf.save(SERIALIZED_TFIDF)

    if os.path.isfile(SERIALIZED_TFIDF_CORPUS):
        corpus_tfidf = corpora.MmCorpus(SERIALIZED_TFIDF_CORPUS)
    else:
        corpus_tfidf = tfidf[corpus]
        corpora.MmCorpus.serialize(SERIALIZED_TFIDF_CORPUS, corpus_tfidf)

    print("loaded tfidf corpus")
    print(len(corpus_tfidf))
    
    if os.path.isfile(SERIALIZED_LSI_CORPUS):
        lsi = models.LsiModel.load(SERIALIZED_LSI_CORPUS)        
    else:
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)
        lsi.save(SERIALIZED_LSI_CORPUS)

    """with open(TOPICS_LIST, "w") as f:
        print(lsi.show_topics(num_topics=-1, num_words=10, log=False, formatted=True), file=f)"""

    corpus_lsi = lsi[corpus_tfidf]
    print(len(corpus_lsi))


    if os.path.exists(SIMILARITY_INDEX):
        index = similarities.MatrixSimilarity.load(SIMILARITY_INDEX)
    else:
        index = similarities.MatrixSimilarity(corpus_lsi, num_features = 200)
        index.save(SIMILARITY_INDEX)

    new_doc = tokenize("""
        When setting a form's opacity should I use a decimal or double?
        <p>I want to use a track-bar to change a form's opacity.</p>

        <p>This is my code:</p>

        <pre><code>decimal trans = trackBar1.Value / 5000;
        this.Opacity = trans;
        </code></pre>

        <p>When I try to build it, I get this error:</p>

        <blockquote>
          <p>Cannot implicitly convert type 'decimal' to 'double'.</p>
        </blockquote>

        <p>I tried making <code>trans</code> a <code>double</code>, but then the control doesn't work. This code has worked fine for me in VB.NET in the past. </p>
""")
    vec_bow = dictionary.doc2bow(new_doc)
    vec_lsi = lsi[vec_bow]
    print("Doc vector in LSI space" + str(vec_lsi))

    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print("**********************")
    print(sims[0:10])

    

if __name__ == "__main__":
    main()
