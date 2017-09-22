# -*- coding: latin-1 -*-
"""
@Michael Jensen
updated 07-09-2017

This script iterates over a series of .xlsx files, and creates a tfidf model

"""
import re
import snowballstemmer
import sys
import numpy as np
import gensim
import pandas as pd
import os
from gensim import corpora


reload(sys)
sys.setdefaultencoding('latin-1')


def any2unicode(string, encoding='latin-1', errors='strict'):
    '''
    :param string: any string
    :param encoding: any encoding you wish
    :param errors: can be set to 'stict' or 'ignore'. Strict will throw error messages at unknown unicode characters
    :return: unicode encoded string
    '''
    if isinstance(string, unicode):
        return string
    return unicode(string, encoding, errors=errors)


to_unicode = any2unicode

def regexp_tokenize(string):
    '''
    :param string:
    :return: string: in lower case, without punctuation
    '''
    string = to_unicode(string)
    string = string.lower()
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(string)


def tokenize(string):
    '''
    :param string:
    :return: string : list of tokens (words as strings)
    '''
    string = regexp_tokenize(string)
    from nltk.corpus import stopwords
    stops = stopwords.words('danish') + stopwords.words('english')
    string = [w.replace(" ", "_") for w in string if w.lower() not in stops]
    lmtzr = snowballstemmer.DanishStemmer()
    string =  lmtzr.stemWords(t for t in string)
    string = [s for s in string if not re.search(r'\d', s)]
    string = [s for s in string if len(s) > 3]
    return string

# iterate over a directory, and yield a tokenized string.
def iter_documents(top_directory):
    '''
    :param top_directory: working directory, which contains a folder called output, with several .xlsx named after topic
    :return: doc_tokenized: tokenized versions of each doc
    '''
    for root, dirs, files in os.walk(top_directory + 'output/'):
        for file in filter(lambda file: file.endswith('.xlsx'), files):
            document = pd.read_excel(os.path.join(root, file))
            doc_string = document['Message'].to_string() # read the entire document, as one big string
            doc_tokenized = tokenize(doc_string)  # or whatever tokenization suits you
            yield doc_tokenized

class MyCorpus(object):
    '''
    Initialize iter_documents()
    '''
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        # self.dictionary.filter_extremes(no_below=1, keep_n=30000) # check API docs for pruning params
        self.dictionary.save('model/dictionary.dict')

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)


def create_model(path):
    '''
    :param path: working directory
    :return: model: tfidf model, dictionary and corpus as Market matrix file, in folder called 'model'
    '''
    if not os.path.exists("model"):
        os.makedirs("model")
    corpus = MyCorpus(path)
    tfidf = gensim.models.TfidfModel(corpus)
    tfidf.save('model/tfidf.model')
    gensim.corpora.MmCorpus.serialize('model/test.mm', corpus)
    print " Created TFIDF model with shape %s" % str(tfidf)



