#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:00:58 2018

@author: nt
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
import gensim

# Read input file:

infile = open('/Users/nt/Documents/Darwin_project/output/all_fields_10.txt', 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")
all_sentences=[]
count=0
for row in input_reader:
    count+=1
    if count <10 and count >1:
        
        fname = row[0]
        date_sent = row[1]
        sender = row[2]
        receiver = row[3]
        letter_text = row[4]
        #print("start"+letter_text+"end")
        
        if letter_text !="":
            
            sentences=sent_tokenize(letter_text)

            #print(fname)
            #print(str(date_sent))
            #print(str(sentences))
            all_sentences.append(sentences)
print(all_sentences)
sentences_tokenized = []
for i in range(len(all_sentences)):
    sentences_tokenized.append([word_tokenize(w) for w in all_sentences[i]])
print(str(sentences_tokenized))
model=gensim.models.Word2Vec(all_sentences, min_count=0)
        
model['identity']
    
    

infile.close()