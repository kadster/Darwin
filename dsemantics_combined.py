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
target_word="British"
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


#define stopwords
stopWords = set(stopwords.words('english'))
#define context words of target one in time_period_1 & 2


#define file names
Transcription='/Users/nt/Documents/Darwin_project/output/final.txt'
outfile =  '/Users/nt/Documents/Darwin_project/output/letters_context_words_'+target_word+'_winsize'+ str(win_size)+'_beyond_sentence_boundary_'+beyond_sentence_boundary+'lemmatize'+lemmatize+'.csv'
vocabulary = dict()


context_word_freq_t1 = dict() #frequency of context word in t1
context_word_freq_t2 = dict() #frequency of context word in t2
#initialize word vector for target word in t1 and t2
target_word_t1 = [] # this is the word vector for target_word in t1; it contains the list of frequencies of co-occurrence
# of context words for target_word in t1; its entries correspond to all vocabulary words
target_word_t2 = [] # this is the word vector for target_word in t2; it contains the list of frequencies of co-occurrence
# of context words for target_word in t2; its entries correspond to all vocabulary words

context_words_t1 = [] #dictionary of all context words of target word in t1; its keys are the context words and its values are
# the frequency with which the context words appear with the target word in t1
context_words_t2 = [] #dictionary of all context words of target word in t2; its keys are the context words and its values are
# the frequency with which the 
#outfile = open('/Users/nt/Documents/Darwin_project/output/more_text.txt', 'w+')

stopWords = set(stopwords.words('english'))

outfile = open(outfile1_file, 'w+')

output_writer1 = csv.writer(outfile1_name, delimiter = "\t")

# write first line of output file 1:

output_writer1.writerow(["Letter_ID","date", "left or right context", "Context words of "+target_word])


# Read input file:

infile = open(Transcription, 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")

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
                    
                    # initialize the list of left context words of all occurrences of the target_word in this letter:

                    left_context = list()

                    # initialize the list of right context words of all occurrences of the target_word in this letter:

                    right_context = list()

                    #find the indices of the target word in the letter:

                    # index_target_word = tokens.index(target_word) # note: this returns the first index (i.e. position)
                    # of target_word in the tokens list of the letter; but the target_word may occur more tha once in
                    # the letter, so we need a list of indices
                    # print(str(index_target_word))
                    indices_target_word = [i for i, x in enumerate(tokens) if x == target_word]
                    
                    # extract all words in the left and right context of the target word:

                    for index_target_word in indices_target_word:  # this loops over all indices of target_word in the letter

                        # tokens[index_target_word-win_size:index_target_word] # this covers the left context of
                        # target_word in case there are at least win_size words to the left of target_word

                        # tokens[max(index_target_word - win_size, 0):index_target_word] # this covers the left context of
                        # target_word also in the case where there are less than win_size words to the left of target_word;
                        # for example, if win_size is 2, and if target_word is the second word in tokens

                        left_context_this_index = tokens[max(index_target_word - win_size, 0):index_target_word] # this
                        # is the list of all words occurring in the left context of this occurrence of the target_word

                        # add the left context words of this occurrence of target_word (indexed by index_target_word)
                        # to left_context:
                        for left_context_word in left_context_this_index:
                            left_context.append(left_context_word)

                            # write context words in output file1:

                            output_writer.writerow([fname, date_sent, "left", left_context_word])

                        # tokens[index_target_word+1:index_target_word+win_size+1] # this covers the right context of
                        # target_word

                        right_context = tokens[index_target_word+1:index_target_word+win_size+1] # this
                        # is the list of all words occurring in the right context of this occurrence of the target_word

                        # add the right context words of this occurrence of target_word (indexed by index_target_word)
                        # to right_context:
                        for right_context_word in right_context:
                            right_context.append(right_context_word)

                            # write context words in output file1:

                            output_writer.writerow([fname, date_sent, "right", right_context_word])

                        # add left context words to the vocabulary:

                        for left_context_word in left_context:

                            if left_context_word in vocabulary:
                                frequency = vocabulary[left_context_word] # this is the frequency of
                                # left_context_word as counted so far
                                frequency += 1 # add 1 to the frequency of left_context_word to account for this
                                # occurrence of left_context_word with target_word
                                vocabulary[left_context_word] = frequency
                            else:
                                vocabulary[left_context_word] = 1

                        # add right context words to the vocabulary:

                        for right_context_word in right_context:
                            if right_context_word in vocabulary:
                                frequency = vocabulary[right_context_word] # this is the frequency of
                                # right_context_word as counted so far
                                frequency += 1 # add 1 to the frequency of left_context_word to account for this
                                # occurrence of right_context_word with target_word
                                vocabulary[right_context_word] = frequency
                            else:
                                vocabulary[right_context_word] = 1

                    #print(vocabulary)
                    
                    print("Letter_ID:", fname)
                    print("left context words:", left_context)

                    print("date:", date_sent)  
                    
                    #check the date of the letter (date_sent) and see whether it is contained in t1 or t2
                    
                    #to do: if the date of the letter is contained in t1 then add context words to context_word_t1
                    # and if it's in t2 ,  add context words to context_word_t2:

                    if date_sent in time_period_1:
                        print("t1:", "the letter was written in t1")

                        # record frequency of left context words in t1 letters:

                        for left_context_word in left_context:
                            if left_context_word in context_words_t1:
                                frequency = context_words_t1[left_context_word]
                                frequency += 1
                                context_words_t1[left_context_word] = frequency
                            else:
                                context_words_t1[left_context_word] = 1

                        print("context_words_t1:",context_words_t1)

                        # record frequency of right context words in t1 letters:

                        for right_context_word in left_context:
                            if right_context_word in context_words_t1:
                                frequency = context_words_t1[right_context_word]
                                frequency += 1
                                context_words_t1[right_context_word] = frequency
                            else:
                                context_words_t1[right_context_word] = 1

                    else:
                        print("t1:", "the letter was not written in t1")

                        
                    if date_sent in time_period_2:
                        print("t2:","the letter was written in t2")

                        # record frequency of left context words in t1 letters:

                        for left_context_word in left_context:
                            if left_context_word in context_words_t2:
                                frequency = context_words_t2[left_context_word]
                                frequency += 1
                                context_words_t2[left_context_word] = frequency
                            else:
                                context_words_t2[left_context_word] = 1

                        print("context_words_t2:", context_words_t2)

                        # record frequency of right context words in t2 letters:

                        for right_context_word in left_context:
                            if right_context_word in context_words_t2:
                                frequency = context_words_t2[right_context_word]
                                frequency += 1
                                context_words_t2[right_context_word] = frequency
                            else:
                                context_words_t2[right_context_word] = 1

                    else:
                        print("t2:", "the letter was not written in t2")


    
outfile.close()
infile.close()