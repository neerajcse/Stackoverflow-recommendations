import os
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

from TextsDAO import TextsDAO
from CorpusDAO import DictionaryDAO
from CorpusDAO import CorpusDAO


DB = "stackoverflow-posts.db"
BASE_DIR = "."
BASE_META_DIR = "."
SERIALIZED_CORPUS = os.path.join(BASE_META_DIR, "corpus.mm")
SERIALIZED_TFIDF = os.path.join(BASE_META_DIR, "tfidf.model")
SERIALIZED_TFIDF_CORPUS = os.path.join(BASE_META_DIR, "corpus_tfidf.mm")

SERIALIZED_LSI_CORPUS = os.path.join(BASE_META_DIR, "corpus_lsi.mm")
TOPICS_LIST = os.path.join(BASE_META_DIR, "list_topics.list")

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

    with open(TOPICS_LIST, "w") as f:
        print(lsi.show_topics(num_topics=-1, num_words=10, log=False, formatted=True), file=f)

    corpus_lsi = lsi[corpus_tfidf]
    print(len(corpus_lsi))
    """
    document = ""
    document = ''.join(e for e in document if e.isalnum() or e == ' ')
    new_doc_bow = dictionary.doc2bow(document.lower().split())
    #print(tfidf[new_doc_bow])

    new_corpus_tfidf = [tfidf[new_doc_bow]]
    lsi.add_documents(new_corpus_tfidf)
    new_corpus_lsi = lsi[new_corpus_tfidf]
    
    doc_count = 0
    topic_count = 0
    for new_doc in new_corpus_lsi:
        doc_count += 1
        print(new_doc)
        for topic_id, coorelation in new_doc:
            if coorelation > 0.05:
                lsi.print_topic(topic_id)
                topic_count += 1
    print("All docs: {} AND Related topics: {}".format(doc_count, topic_count))
    """

if __name__ == "__main__":
    main()