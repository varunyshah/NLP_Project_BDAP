
# coding: utf-8

import os
import csv
import nltk as nt
import numpy as np
import pandas as pd
from nltk import pos_tag
import nltk.tag.stanford as ST
from nltk.corpus import stopwords
from nltk.tag import StanfordNERTagger
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize,word_tokenize


### Global Lists
clean_token = []
final_words = []


### Reading Tweets from csv File
with open('agriculture.csv') as csvfile:
    raw = []
    data = csv.DictReader(csvfile)
    for row in data:
         raw.append(row['text'])

### Removing garbage value from Tweets        
tokenizer = RegexpTokenizer(r'\w+')  

### Tokenizing ,Tagging and removing Stop words from tweets
for i in range(len(raw)):
    clean_token = tokenizer.tokenize(raw[i])
    java_path = "C:/Program Files/Java/jdk1.8.0_111/bin"
    os.environ['JAVAHOME'] = java_path
    tagger = ST.StanfordNERTagger('.../stanford-ner-2014-06-16/stanford-ner-2014-06-16/classifiers/english.conll.4class.distsim.crf.ser.gz',
                       '.../stanford-ner-2014-06-16/stanford-ner-2014-06-16/stanford-ner.jar',encoding = 'utf-8')
    mytweet_tag = tagger.tag(clean_token)
    stop = set(stopwords.words('english'))
    without_stop= [i for i in mytweet_tag if i not in stop]
    final_words.append(without_stop)
    
     
### # Tag tokens with standard NLP BIO tags
bio_tagged = []
prev_tag = "O"
for i in range(len(final_words)):
    for token, tag in final_words[i]:
        if tag == "O":
            bio_tagged.append((token,tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":
            bio_tagged.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:
            bio_tagged.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:
            bio_tagged.append((token, "B-"+tag))
            prev_tag = tag
  
 ### Create Tree
def stanford_tree(bio_tagged):
	tokens, ne_tags = zip(*bio_tagged)
	pos_tags = [pos for token, pos in pos_tag(tokens)]
	conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
	ne_tree = conlltags2tree(conlltags)
	return ne_tree
 
 #ne_treee = stanford_tree(bio_tagged)
### Parse named entities from tree
def structure_ne(ne_tree):
	ne = []
	for subtree in ne_treee:
		if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
			ne_label = subtree.label()
			ne_string = " ".join([token for token, pos in subtree.leaves()])
			ne.append((ne_string, ne_label))
	return ne
 
### Grouping all Functions
def stanford_main():
	print(structure_ne(stanford_tree(bio_tagged)))


### Main Function
if __name__ == '__main__':
	stanford_main()








