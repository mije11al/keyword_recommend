# -*- coding: latin-1 -*-
"""
@Michael Jensen

updated 05-09-2017

This script uses a gensim tfidf model to generate keyword recommendations.

"""


import pickle
import gensim
from gensim import corpora
import os
import pandas as pd
import re
import snowballstemmer
import data_preprocessing as dp


def any2unicode(string, encoding='latin-1', errors='strict'):
    '''
    :param string: any string
    :param encoding: any encoding you wish
    :param errors: can be set to 'strict' or 'ignore'. Strict will throw error messages at unknown unicode characters.
    :return: unicode encoded string
    '''
    if isinstance(string, unicode):
        return string
    return unicode(string, encoding, errors=errors)


to_unicode = any2unicode

def regexp_tokenize(string):
    '''
    :param string:
    :return: string, without punctuation
    '''
    string = to_unicode(string)
    string = string.lower()
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(string)


def tokenizer(string):
    '''
    :param string:
    :return: string : list of tokens (words as strings)
    '''
    string = regexp_tokenize(string)
    from nltk.corpus import stopwords
    stops = stopwords.words('danish') + stopwords.words('english')
    string = [w.replace(" ", "_") for w in string if w.lower() not in stops]
    string = [s for s in string if not re.search(r'\d', s)]
    string = [s for s in string if len(s) > 3]
    lmtzr = snowballstemmer.DanishStemmer()
    tokens =  lmtzr.stemWords(t for t in string)
    return tokens


def coherence(list, dictionary):
    '''
    :param list: list of lists of word recommendations
    :param dictionary: gensim dictionary
    :return: coherence score pr. list in list of lists
    '''
    new_list = []
    for sublist in list:
        nsublist = [item[0] for item in sublist]
        new_list.append(nsublist)
    cm = gensim.models.coherencemodel.CoherenceModel(topics=new_list,
                                                     corpus=corpora.MmCorpus('model/test.mm') ,
                                                     dictionary=dictionary,
                                                     coherence='u_mass')
    return cm.get_coherence_per_topic()


def recommendations(n):
    '''
    :param n: integer describing number of recommendations wanted
    :return rec: list of lists, contains coherence scores + word recommendations
    '''
    all=[]
    tfidf = gensim.models.TfidfModel.load(('model/tfidf.model'))
    corpus = corpora.MmCorpus('model/test.mm')
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        ls = []
        doc = sorted(doc, key=lambda x: x[1], reverse=True)
        # cut off docs in the next line, to reduce runtime.
        doc = doc[:n]
        dictionary = corpora.Dictionary.load('model/dictionary.dict')
        for id, value in doc:
            word = dictionary.get(id)
            tup = (word, value)
            ls.append(tup)
        all.append(ls)
    cm = coherence(all,dictionary)
    recs = zip(cm,all)
    return recs


def create_dict(recs):
    '''
    :param recs: list of lists, contains coherence scores + word recommendations
    :return: rec_dict: recs as dict, with topic names as key
    '''
    names = dp.topic_names(os.getcwd())
    rec_dict = {x: list(y) for x, y in zip(names, recs)}
    return rec_dict


def create_filtered_recommendations_dictionary(path, n):
    '''
    :param path: path containing topic_index.xlsx file
    :param n: number of recommendations wanted
    :return: newdict: dict of recommendations, without words already in topic_index.xlsx
    '''
    newdict = {}
    recs = recommendations(n)
    dict = create_dict(recs)
    for k, v in dict.items():
        cm = v[:1]
        ls = v[1:]
        priors = []
        df = pd.read_excel(path + 'topic_index.xlsx',
                           sheetname='keywords')
        for column in df:
            string = df[column].to_string()
            words = tokenizer(string)
            priors.append(words)
        flat_priors=[item for sublist in priors for item in sublist]
        vnew = [i for i in ls if i[0] not in flat_priors]
        newdict[k] = cm + vnew
    print "List of recommendations is now done!"
    return newdict






