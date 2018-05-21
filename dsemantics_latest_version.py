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

#define parameters
target_word="species"
#define time intervals
time_period_1=list(range(1807,1858))
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

context_word_freq_t1=dict() #frequency of context word in t1 
context_word_freq_t2=dict() #frequency of context word in t2
#initialize word vector for target word in t1 and t2
target_word_t1=[]
target_word_t2=[]
#define file names
Transcription='/Users/nt/Documents/Darwin_project/output/final.txt'
# All the strings for output:
Letter_ID =""                    
date=int
t1=""
context_words_t1=[] #list of all context words of target word in t1
t2=""
context_words_t2=[] #list of all context words of target word in t2
# Open output file:
outfile = open('/Users/nt/Documents/Darwin_project/output/more_text.txt', 'w+')
output_writer = csv.writer(outfile, delimiter = "\t")
output_writer.writerow(["Letter_ID","date","context words","context_voc","t1","context_words_t1", "t2","context_words_t2"])
# Read input file:
infile = open(Transcription, 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")
output_strs = []

#all_sentences=[]
count=0
for row in input_reader:
    count+=1
    if count <8000 and count >1:
        
        fname = row[0]
        date_sent = int(row[1])
        sender = row[2]
        receiver = row[3]
        letter_text = row[4]
        #print("start"+letter_text+"end")
        context_voc=[]
        vocabulary=[]
        if target_word in letter_text:            
            sentences=sent_tokenize(letter_text)
             
            #to do: replace m r . with mr. and other titles                         
            old_titles = ('D r .', 'M r .', 'M r', 'I', 'The')
            new_titles = ('Dr.', 'Mr.', 'Mr.', '', '')

            for i in range(len(old_titles)):
                letter_text = letter_text.replace(old_titles[i],new_titles[i])
            #print(letter_text)                       
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
                    context_voc.append(((vocabulary[index_target_word-win_size+1:index_target_word]),vocabulary[index_target_word+1:index_target_word+win_size]))
                    #print(vocabulary)
                    
                    print("Letter_ID:", fname)
                    print("context words:", context_voc)
                    print("date:", date_sent)  
                    
                    
                    #to do: check the date of the letter (date_sent) and see whether it is contained in t1 or t2
                    
                    #to do: if the date of the letter is contained in t1 then add context words to the list context_word_t1 and if it's in t2 , do the same thing                        
                    if date_sent in time_period_1:
                                    #range(1823, 1858)
                        print("t1:", "yes")
                   #     for word in context_voc:
                   #         context_words_t1.append(word)
                   #     print("context_words_t1:",context_words_t1)
                    else: print("t1:", "no")
                                            
                    if date_sent in time_period_2:
                        print("t2:", "yes")
                  #      for word in context_voc:
                  #          context_words_t2.append(word)
                  #      print("context_words_t2:",context_words_t2)
                    else: print("t2:", "no")
                  
                    #to do: if the date of the letter is contained in t1, for every context word define the dictionary context_word_freq_t1 with key as the context word and value as the frequency
                        #if 'nature' is a context word then do context_word_freq_t1['nature']=1
                        #for now all frequencies will be 1, next time discuss how to deal with frequencies greater than 1
                        
                    #for context_word in context_words_t1:
                     #   context_word_freq_t1[context_word] = 1
                        
                    #for context_word in context_words_t2:
                     #   context_word_freq_t2[context_word] = 1
                    
                    
                    #print(context_word_freq_t1)
                    
                                        
                   #extract word vectors for target word in t1 and t2       
#                     for word in vocabulary:
#                       if word in context_words_t1:
#                           target_word_t1.append(context_word_freq_t1[word])
#                       elif word in context_words_t2:
#                           target_word_t2.append(context_word_freq_t2[word])   
                    
                    #calculate cosine distance between word vectors for t1 and t2
                    
#                    cosine_distance = 1 - spatial.distance.cosine(target_word_t1, target_word_t2)     
#                    print('cosine_distance', str(cosine_distance))'''
                                 

    
                output_writer.writerow([fname, context_voc, date_sent, t1, context_words_t1, t2, context_words_t2]) 

infile.close()