# -*- coding: latin-1 -*-

"""
@Michael Jensen

updated 22-09-2017

This script is a wrapper, which sorts a vector of texts into topics, based on seed keywords.
It returns a series of .xlsx files with texts sorted into topics, a visualization describing topics in terms of size,
features and intertopic distance. It also provides recommendations for new keywords, and scores for topic cohesion.


It requires an .xlsx file called topic_index.xlsx, with a sheet named "keywords", containing a series of named topic vectors with keywords.
"""

import emner_v3
import pandas as pd
import tfidf_generator
import glob
import os
import kw_recommendations as k_recs
import data_preprocessing as dp
import gensim_pyLDAvis as vis
import time

path = "/Users/nextwork/Dropbox/PycharmProjects/topics/"



def get_topics(path): # This step is optional for local work. Just make sure that the last line recieves a pandas dataframe.
    '''
    :param path: your working directory, a path containing an .xlsx file with data
    :return: you data, sorted into .xlsx files named after topics, in a folder called output.
    '''
    #all_files = glob.glob(os.path.join
                          #(path, "input/*.xlsx"))
    all_files = glob.glob(os.path.join
                          (path, "input/test/*.xlsx")) # in case you want to run a smaller test with samples.

    for f in all_files:
        dfs = pd.read_excel(f)
        dfs = dfs[pd.notnull(dfs['Message'])] # remove leftover NaN values in dataframe
        #dfs = dfs.sample(n=2000) # in case you want to run a smaller test with samples.
        #dfs.to_excel(path + '/input/test/test.xlsx')
        print "Number of posts: %d" %len(dfs)
        emner_v3.dagsordener(dfs) # Takes a dataframe


def visualize(path):
    '''
    :param path: your working directory
    :return: an .html file with a pyLDAvis visualization of topics.
    '''
    tfidf_generator.create_model(path)
    dp.runner(path)
    vis.runner(path)

def kw_recs(path, n):
    '''
    :param path: your working directory
    :param n: number of new keyword recommendations wanted
    :return: a dictionary of keyword recommendations.
    '''
    recs = k_recs.create_filtered_recommendations_dictionary(path, n)
    dp.pickle_writer(path,"keyword_recommendations",recs)



if __name__ == '__main__':
    start = time.time()
    get_topics(path)
    visualize(path)
    kw_recs(path, 3)
    end = time.time()
    print(end - start)