#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 12:00:58 2018

@author: nt
"""
#import modules
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
from scipy import spatial

#define parameters
target_word="evolution"
time_period_1=[1823,1858]
time_period_2=[1859,1882]
win_size= 2
#context words occurring with target word go beyond sentence boundary
beyond_sentence_boundary="yes"
#lemmatize yes or no
lemmatize="no"

#define vocabulary

vocabulary=[]

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
                if lemmatize == "no":
                
                    tokens = word_tokenize(letter_text)
                    print("tokens", str(tokens))
                    #extract target word from the letters
            
                    #to do: loop over the list of tokens by index and find the index of the target word
                    for target_word_t1 in time_period_1:
                        if target_word_t1 in time_period_2:
                            time_period_2.index(target_word_t2)[1] += 1
                        else:
                            time_period_2.append([target_word_t1,0])
                    
                    #to do: define the range for the left and right context of the target word
                            
                                
                    #to do: extract all words in the left and right context of the target word
                        def search(target_word_t1, context=4):

                            matches = (i for (i,w) in enumerate(target_word_t1) if w.lower() == target)
                                    for index in matches:
                                        if index < context //2:
                                            yield words[0:context+1]
                                        elif index > len(words) - context//2 - 1:
                                            yield words[-(context+1):]
                                        else:
                                            yield words[index - context//2:index + context//2 + 1]
                                            
                      print(list(search('target_word_t1', text)))                  
                                                
                    #to do: add these words to the vocabulary list
                    
                    
                    #to do: check the date of the letter (date_sent) and see whether it is contained in t1 or t2
                    
                    
                    #to do: if the date of the letter is contained in t1 then add context words to the list context_word_t1 and if it's in t2 , do the same thing
                    #to do: if the date of the letter is contained in t1, for every context word define the dictionary context_word_freq_t1 with key as the context word and value as the frequency
                        #if 'nature' is a context word then do context_word_freq_t1['nature']=1
                        #for now all frequencies will be 1, next time discuss how to deal with frequencies greater than 1
                    

#extract word vectors for target word in t1 and t2       
for word in vocabulary:
   if word in context_words_t1:
       target_word_t1.append(context_word_freq_t1[word])
   elif word in context_words_t2:
       target_word_t2.append(context_word_freq_t2[word])   

#calculate cosine distance between word vectors for t1 and t2

cosine_distance = 1 - spatial.distance.cosine(target_word_t1, target_word_t2)     
print('cosine_distance', str(cosine_distance))
             
                        
                        
                        
                        
                        
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