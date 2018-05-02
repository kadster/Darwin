#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:00:58 2018

@author: nt
"""
#import modules
from nltk.tokenize import sent_tokenize, word_tokenize
import csv

#define parameters
target_word="evolution"
time_period_1=[1823,1858]
time_period_2=[1859,1882]
win_size= 2
#context words occurring with target word go beyond sentence boundary
beyond_sentence_boundary="yes"

#define vocabulary

vocabulary=[]

#define file names

Transcription='/Users/nt/Documents/Darwin_project/output/all_fields_10.txt'

# Read input file:

infile = open(Transcription, 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")

#all_sentences=[]
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
            #print(letter_text)
            #to do: replace m r . with mr. and other titles
            
            if beyond_sentence_boundary == "yes":
                #tokenize letter_text
                
                tokens =word_tokenize(letter_text)
                print("tokens", str(tokens))
                #extract target word from the letters
            
                #to do: loop over the list of tokens by index and find the index of the target word
                #to do: define the range for the left and right context of the target word
                
            
#extract the vocabulary from the corpus



#extract word vectors for target word in t1 and t2            
#            
#            all_sentences.append(sentences)
#print(all_sentences)
#sentences_tokenized = []
#for i in range(len(all_sentences)):
#    sentences_tokenized.append([word_tokenize(w) for w in all_sentences[i]])
#print(str(sentences_tokenized))
#model=gensim.models.Word2Vec(all_sentences, min_count=0)
        
#model['identity']
    
    

infile.close()