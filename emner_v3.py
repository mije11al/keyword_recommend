# -*- coding: latin-1 -*-
"""
@Michael Jensen

updated 22-09-2017

This script sorts strings into .xlsx files named after topics defined in a doc called
'topic_index.xlsx'

"""

import pandas as pd
import os, re
import glob
import numpy as np

# ==============================================================================
import sys

reload(sys)
sys.setdefaultencoding('latin-1')


def splitter(df):
    '''
    :param df: a dataframe, with one vector of strings named 'Message', and 1/0 values for each topic
    :return: a series of .xlsx files sorted into topics
    '''
    df = df.loc[:, ~(df == 0).all()]
    print "Number of posts sorted into topics: %d" % len(df[df.sum(axis=1) > 0])
    for column in df:
       filter=df.loc[df[str(column)] == 1]
       new_df=filter[['Message', str(column)]]
       print column + ' contains %d' % len(new_df)
       if len(new_df) < 3:                   # solve bug where 'Message' becomes a topic column
           pass
       else:
           new_df.to_excel("output/" + column +
            ".xlsx", columns=['Message'])


def dagsordener(df):
    '''
    :param df: a dataframe, with one vector of strings named 'Message'
    :return: a dataframe, with one vector of strings named 'Message', and 1/0 values for each topic, which is passed to splitter()
    '''
    index = pd.read_excel('topic_index.xlsx',
    sheetname='keywords')
    topic_names = list(index.columns)
    index = index.replace(np.nan, "{}", regex=True)
    for column in index.columns:                        # create new topic columns in dataframe, named after topic_index.xlsx columns, with numerical bool values
        df[column] = df['Message'].str.contains\
                                       ('|'.join(map(re.escape,
                                       index[column].values, )))
    print "Done with sortation"
    df_num = df.loc[:, topic_names[0]:].applymap \
                                         (lambda x: 1 if x else 0)
    df = df_num.combine_first(df)
    print "(message, topic) dataframe has been completed"
    return splitter(df)



