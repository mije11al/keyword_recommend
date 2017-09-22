#  Topic sortation by keyword


This repo contains tools for sorting Facebook text data into topics,
based on manually seeding keywords. 



Running wrapper.py returns a series of .xlsx files with texts sorted into topics, a visualization describing topics in terms of size,
features and intertopic distance. It also provides recommendations for new keywords, and scores for topic cohesion.



## Getting started 


### Prerequisites

The scripts here require the following.

* A folder with same structure as the repo.
* An .xlsx file called topic_index.xlsx, with a sheet named "keywords", containing a series of named topic vectors with keywords. Look at the current file for an example
* Any .xlsx file containing a vector of strings, with 'Message' as head.

### Package requirements

to run the script, you need :
```
gensim 
pyLDAvis 
pandas
NLTK
sklearn
pickle
optionally snowball stemmer, for tokenization.
```


## Usage


### Running the script
Open up wrapper.py, and fill out your path variable, or setup a DB connection. Directions are commented in the script

run wrapper.py in terminal/powershell
```
python2.7 wrapper.py
```

Run the script, and you should have end up with a nice visualisation of your topics, and a pickled dict
of cohesion scores and new keyword recommendations pr. topic.


## Authors

* **Michael Jensen** - *First draft* - [mije11al](https://github.com/mije11al)
* **Haavard Lundberg** - *Yet to be seen!* - [havardl](https://github.com/havardl)

