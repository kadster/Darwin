#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:00:58 2018

@author: nt
"""
#import modules
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import csv
from scipy import spatial
#import re
#import pandas as pd
#pd.interval_range(start='1823-01-01', end='1858-01-01')
#time_period_1= pd.interval_range#
#print(time_period_1)
#data = pd.date_range([0, 1, 2, 3], index=index)
#print(data)       

#define parameters
target_word="brain"
#define time intervals
#date_t1_1=1823
#date_t1_2=1858

time_period_1=list(range(1823,1858))
time_period_2=list(range(1859,1882))

#define window size
win_size= 3
#context words occurring with target word go beyond sentence boundary
beyond_sentence_boundary="yes"
#lemmatize yes or no
lemmatize="no"
#define vocabulary
vocabulary=[]
#define stopwords
stopWords = set(stopwords.words('english'))
#define context words of target one in time_period_1 & 2
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
Letter_ID =""                    
date=int
t1=""
t2=""
# Open output file:
outfile = open('/Users/nt/Documents/Darwin_project/output/ds.txt', 'w+')
output_writer = csv.writer(outfile, delimiter = "\t")
output_writer.writerow(["Letter_ID","context words","date","t1", "t2"])
# Read input file:
infile = open(Transcription, 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")
output_strs = []


#all_sentences=[]
count=0
for row in input_reader:
    count+=1
    if count <10 and count >1:
        
        fname = row[0]
        date_sent = int(row[1])
        sender = row[2]
        receiver = row[3]
        letter_text = row[4]
        #print("start"+letter_text+"end")
        
        if letter_text !="" and target_word in letter_text:
            
            sentences=sent_tokenize(letter_text)
             
            #to do: replace m r . with mr. and other titles  
            
           
            old_titles = ('D r .', 'M r .', 'M r', 'I', 'The')
            new_titles = ('Dr.', 'Mr.', 'Mr.', '', '')

            for i in range(len(old_titles)):
                letter_text = letter_text.replace(old_titles[i],new_titles[i])
            
            '''letter_text = letter_text.replace('D r .', 'Dr.')
            letter_text = letter_text.replace('M r .', 'Mr.')
            letter_text = letter_text.replace('M r', 'Mr.')
            #letter_text = letter_text.replace('&', ' ')
            letter_text = letter_text.replace('I', ' ')
            letter_text = letter_text.replace('The', ' ')
            #letter_text = letter_text.replace('"', ' ')'''
            #print(letter_text)
            #prints 'Goodbye everyone. Say "Goodbye" to me!'
            
            if beyond_sentence_boundary == "yes":
                #tokenize letter_text
                if lemmatize == "no":
                
                    tokens = word_tokenize(letter_text)
                    #remove punctuation
                    tokenizer = RegexpTokenizer(r'\w+')
                    tokens = tokenizer.tokenize(letter_text)
                    #print("tokens", str(tokens))
                    #print(len(tokens))
                    #print(stopWords)
                    #print(len(stopWords))
                                      
                    #substract stopwords from tokens
                    for t in tokens:
                        if t not in stopWords:
                            vocabulary.append(t)                                                                                      
                    #print(vocabulary)
                    #print(len(vocabulary))
                    
                    #find the index of the target word
                    index_target_word=vocabulary.index(target_word)
                    #print(str(index_target_word))
                    
                    #to do: define the range for the left and right context of the target word
                    #print(vocabulary[index_target_word-win_size+1:index_target_word][0])
                    #print(vocabulary[index_target_word+1:index_target_word+win_size])
                    
                         #to do: extract all words in the left and right context of the target word
                         #to do: add these words to the vocabulary list 
                    vocabulary=((vocabulary[index_target_word-win_size+1:index_target_word]),vocabulary[index_target_word+1:index_target_word+win_size])
                    #print(vocabulary)
                    
                    print("Letter_ID:", fname)
                    print("context words:", vocabulary)
                    print("date:", date_sent)  
                    
                    #to do: check the date of the letter (date_sent) and see whether it is contained in t1 or t2
                    
                    #to do: if the date of the letter is contained in t1 then add context words to the list context_word_t1 and if it's in t2 , do the same thing                        
                    if date_sent in time_period_1:
                                    #range(1823, 1858)
                        print("t1:", "yes")
                        context_words_t1.append(target_word)
                        print("context_word_t1:",context_words_t1)
                    else: print("t1:", "no")

                        
                    if date_sent in time_period_2:
                        print("t2:", "yes")
                        context_words_t2.append(target_word)
                    else: print("t2:", "no")
                  
            #is this necessary?      
            #to do: if the date of the letter is contained in t1 then add context words to the list context_word_t1 and if it's in t2 , do the same thing    
                        
                    
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

infile.close()