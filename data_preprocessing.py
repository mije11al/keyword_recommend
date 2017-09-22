# -*- coding: latin-1 -*-
"""
@Michael Jensen

updated 22-09-2017

This script iterates over data in your directory, and outputs a series of files that are needed to create
a pyldavis visualization that is compatible with a tfidf model.

"""


import gensim
from gensim import corpora
import pandas as pd
import glob, os
import re
import snowballstemmer
import sys
from operator import itemgetter
import pickle




# convert any string to unicode.
def any2unicode(string, encoding='latin-1', errors='strict'):
    '''
    :param string: any string
    :param encoding: any encoding you wish
    :param errors: can be set to 'strict' or 'ignore'. Strict will throw error messages at unknown unicode characters
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
    # tokenize + punctuation
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


def topic_names(path):
    '''
    :param path: working directory, with topic .xlsx files
    :return: list of topic names
    '''
    names = []
    all_files = glob.glob(os.path.join(path,'output/*.xlsx'))
    for f in all_files:
        filename = os.path.basename(f)
        newname = str(filename)[:-5]
        names.append(newname)
    return names


def pickle_writer(path, name, var):
    '''

    :param path: working directory
    :param name: whatever name you want the file to have
    :param var: any given variable
    :return: pickled variable in path
    '''
    with open (path + name + ".pickle", 'wb') as handle:
        pickle.dump(var, handle, protocol=pickle.HIGHEST_PROTOCOL)


def create_doc_topic_dists(path):
    '''

    :param path: working directory, with topic .xlsx files
    :return:  matrix with document, topic distributions, as .xslx file. topic dist is assumed to be 100% for each document.
    '''
    names = topic_names(path)
    names2 = topic_names(path)

    df = pd.DataFrame(data=0, index = names, columns = names2)

    for column in df.columns:
        for index in df.index:
            if column == index:
                df[column].loc[[index]] = 1
            else:
                df[column].loc[[index]] = 0
    if not os.path.exists(path + "data_for_visualization"):
        os.makedirs(path + "data_for_visualization")
    return df.to_excel(path + '/data_for_visualization/doc_topic_dists.xlsx')


def len_doc(path):
    '''
    :param path: working directory, with topic .xlsx files
    :return: pickled list of document lengths.
    '''
    all_files = glob.glob(os.path.join(path, 'output/*.xlsx'))
    len_doc = []
    for f in all_files:
        document = pd.read_excel(f)
        doc_string = document['Message'].to_string()
        doc_tokenized = tokenize(doc_string)
        len_doc.append(len(doc_tokenized))

    return pickle_writer(path, "/data_for_visualization/len_doc",len_doc)



def vocab(path, dictionary):
    '''
    :param path: working directory, with topic .xlsx files
    :param dictionary: gensim dictionary
    :return: pickled list with complete vocabulary for corpus, sorted by tfidf ID
    '''
    vocab = []
    for k, v in dictionary.iteritems():
        vocab.append((k, v))
        vocab = sorted(vocab, key=lambda x: x[0], reverse=False)

    pickle_writer(path, "/data_for_visualization/vocab",vocab)


def freqlist(path, dictionary, corpus):
    '''
    :param path: working directory, with topic .xlsx files
    :param dictionary: gensim dictionary
    :param corpus: corpus as Market matrix file
    :return: pickled list of of word to frequency tupless
    '''
    n = len(dictionary)
    freq = [0] * n
    for vector in corpus:
        for element in vector:
            freq[element[0]] += element[1]

    # Sort the tokens alphabetically
    freqlist = [None] * n
    for i in range(n):
        freqlist[i] = (i, dictionary[i], freq[i])
    freqlist = sorted(freqlist, key=itemgetter(1))
    return pickle_writer(path, "/data_for_visualization/freqlist", freqlist)



def runner(path):
    '''

    :param path: working directory
    :return: pyLDAvis visualisation, as .html file
    '''
    dictionary = corpora.Dictionary.load(path + 'model/dictionary.dict')
    corpus = corpora.MmCorpus(path + 'model/test.mm')
    create_doc_topic_dists(path)
    len_doc(path)
    vocab(path, dictionary)
    freqlist(path, dictionary,corpus)
    print "Data for pyLDAvis is now ready!"