#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:00:58 2018

@author: nt
"""
#import modules
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import csv
from scipy import spatial
import pandas as pd
pd.interval_range(start='1823-01-01', end='1858-01-01')
#time_period_1= pd.interval_range#
#print(time_period_1)
#data = pd.date_range([0, 1, 2, 3], index=index)
#print(data)

#define parameters
target_word="identity"
time_period_1=[1823,1858]
time_period_2=[1859,1882]
win_size= 3
#context words occurring with target word go beyond sentence boundary
beyond_sentence_boundary="yes"
#lemmatize yes or no
lemmatize="no"

#define vocabulary

vocabulary=[]

#define stopwords
stopWords = set(stopwords.words('english'))
#wordsFiltered = []

#to do: define context words of target one in time_period_1 & 2
context_words_t1=[] #list of all context words of target word in t1
context_words_t2=[] #list of all context words of target word in t2
context_word_freq_t1=dict() #frequency of context word in t1 
context_word_freq_t2=dict() #frequency of context word in t2

#initialize word vector for target word in t1 and t2
target_word_t1=[]
target_word_t2=[]


#define file names

Transcription='/Users/nt/Documents/Darwin_project/output/all_fields_10.txt'


# All the strings for output:


# Open output file:



# Read input file:

infile = open(Transcription, 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")
output_strs = []
outfile = open('/Users/nt/Documents/Darwin_project/output/ds.txt', 'w+')
output_writer = csv.writer(outfile, delimiter = "\t")
output_writer.writerow(["Letter_ID","context words","date","t1", "t2"])

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
        
        if letter_text !="" and target_word in letter_text:
            
            sentences=sent_tokenize(letter_text)
            #print(letter_text)
            #to do: replace m r . with mr. and other titles
            
            
            if beyond_sentence_boundary == "yes":
                #tokenize letter_text
                if lemmatize == "no":
                
                    tokens = word_tokenize(letter_text)
                    #print("tokens", str(tokens))
                    #extract target word from the letters
                    #print(len(tokens))
                    #show stop words
                    #print(stopWords)
                    
                    #print(len(stopWords))
                    #print tokens without stopwords
                    
                    #substract stopwords from tokens
                    for t in tokens:
                        if t not in stopWords:
                            vocabulary.append(t)
                    
                    
                    
                    #print(vocabulary)
                    #print(len(vocabulary))
                    #to do: loop over the list of tokens by index and find the index of the target word
                    index_target_word=vocabulary.index(target_word)
                    
                    #print(str(index_target_word))
                    
                    #to do: define the range for the left and right context of the target word
                    #print(vocabulary[index_target_word-win_size+1:index_target_word])
                    #print(vocabulary[index_target_word+1:index_target_word+win_size])
                    
                         #to do: extract all words in the left and right context of the target word
                         #to do: add these words to the vocabulary list 
                    vocabulary=((vocabulary[index_target_word-win_size+1:index_target_word]),vocabulary[index_target_word+1:index_target_word+win_size])
                    
                    Letter_ID =""                    
                    date=""
                    t1="yes"
                    t2="no"
                    
                
                    print("Letter_ID:", fname)
                    print("context words:", vocabulary)
                    print("date:", date_sent)  
                    
                    #to do: check the date of the letter (date_sent) and see whether it is contained in t1 or t2
                    
                    
                    
                    if date_sent in time_period_1:
                        print("t1:", "yes")
                    else: print("t1:", "no")
                        
                    if date_sent in time_period_2:
                        print("t2:", "yes")
                    else: print("t2:", "no")
                        
                     
                    
                    #to do: if the date of the letter is contained in t1 then 
                    #add context words to the list context_word_t1 and if it's in t2 , do the same thing    
                    
                    
                    
                    
                    #To do: find adjustment for when the window of the target word is smaller than window size                   
                               
                   
                    
                               
                      
                    
                    
                    
                    
                    
                    #to do: if the date of the letter is contained in t1, for every context word define the dictionary context_word_freq_t1 with key as the context word and value as the frequency
                        #if 'nature' is a context word then do context_word_freq_t1['nature']=1
                        #for now all frequencies will be 1, next time discuss how to deal with frequencies greater than 1
                    

#extract word vectors for target word in t1 and t2       
#for word in vocabulary:
#   if word in context_words_t1:
#       target_word_t1.append(context_word_freq_t1[word])
#   elif word in context_words_t2:
#       target_word_t2.append(context_word_freq_t2[word])   

#calculate cosine distance between word vectors for t1 and t2

#cosine_distance = 1 - spatial.distance.cosine(target_word_t1, target_word_t2)     
#print('cosine_distance', str(cosine_distance))
             
                        
                        
                        
                        
                        
#            
#            all_sentences.append(sentences)
#print(all_sentences)
#sentences_tokenized = []
#for i in range(len(all_sentences)):
#    sentences_tokenized.append([word_tokenize(w) for w in all_sentences[i]])
#print(str(sentences_tokenized))
#model=gensim.models.Word2Vec(all_sentences, min_count=0)
        
#model['identity']
    
                output_writer.writerow([fname, vocabulary, date_sent, t1, t2]) 
'''
infile.close()