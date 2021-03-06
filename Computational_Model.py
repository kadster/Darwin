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

#define parameters:

target_word = "evolution"
#define time intervals
#date_t1_1=1823
#date_t1_2=1858

time_period_1 = list(range(1822,1859))
time_period_2 = list(range(1860,1882))

#define window size
win_size = 5
#context words occurring with target word go beyond sentence boundary
beyond_sentence_boundary = "yes"
#lemmatize yes or no
lemmatize = "no"


#define file names:

Transcription = '/Users/nt/Documents/finalfinal.txt'
outfile1_name = '/Users/nt/Documents/Darwin_project/output/letters_context_words_'+target_word+'_winsize-'+ str(win_size)+'_beyond_sentence_boundary-'+beyond_sentence_boundary+'lemmatize-'+lemmatize+'.csv'
outfile2_name = '/Users/nt/Documents/Darwin_project/output/word_vectors_'+target_word+'_winsize'+ str(win_size)+'_beyond_sentence_boundary_'+beyond_sentence_boundary+'lemmatize'+lemmatize+'.txt'
outfile3_name = '/Users/nt/Documents/Darwin_project/output/cosine_distance_word_vectors_'+target_word+'_winsize'+ str(win_size)+'_beyond_sentence_boundary_'+beyond_sentence_boundary+'lemmatize'+lemmatize+'.txt'


#define vocabulary, which is a dictionary whose keys are all context words of the target_word and whose values are their
# frequency of their co-occurrence with the target_word:
vocabulary = dict()
vocabulary_list = [] # this is the list of all vocabulary words

#initialize word vector for target word in t1 and t2
target_word_t1 = [] # this is the word vector for target_word in t1; it contains the list of frequencies of co-occurrence
# of context words for target_word in t1; its entries correspond to all vocabulary words
target_word_t2 = [] # this is the word vector for target_word in t2; it contains the list of frequencies of co-occurrence
# of context words for target_word in t2; its entries correspond to all vocabulary words

context_words_t1 = dict() #dictionary of all context words of target word in t1; its keys are the context words and its values are
# the frequency with which the context words appear with the target word in t1
context_words_t2 = dict() #dictionary of all context words of target word in t2; its keys are the context words and its values are
# the frequency with which the context words appear with the target word in t2


# define stopwords:

stopWords = set(stopwords.words('english'))

# Open output1 file, which contains the list of context words of target_word in each letter:
outfile1 = open(outfile1_name, 'w+')

output_writer1 = csv.writer(outfile1, delimiter = "\t")

# write first line of output file 1:

output_writer1.writerow(["date", "left or right context", "Context words of "+target_word])


# Read input file:

infile = open(Transcription, 'r+', encoding='utf-8')
input_reader = csv.reader(infile, delimiter = "\t")


count = 0
for row in input_reader:
    count += 1
    if count >1 and count < 5477: # 5477 is the maximum number of lines
        #print(str(count))
        fname = row[0]
        date_sent = int(row[1])
        sender = row[2]
        receiver = row[3]
        letter_text = row[4]
        #print(letter_text)
        
        if letter_text != "" and target_word in letter_text:

            letter_text = letter_text.lower()
            sentences=sent_tokenize(letter_text)
             
            #to do: replace m r . with mr. and other titles  
            
           
            old_titles = ('D r .', 'M r .', 'M r', 'I', 'The')
            new_titles = ('Dr.', 'Mr.', 'Mr.', '', '')

            for i in range(len(old_titles)):
                letter_text = letter_text.replace(old_titles[i],new_titles[i])
            #print(letter_text)
           
            
            if beyond_sentence_boundary == "yes":

                #tokenize letter_text:

                if lemmatize == "no":
                
                    tokens = word_tokenize(letter_text)

                    #remove punctuation
                    tokenizer = RegexpTokenizer(r'\w+')
                    tokens = tokenizer.tokenize(letter_text)
                    #print("tokens", str(tokens))
                    #print(len(tokens))
                    #print(stopWords)
                    #print(len(stopWords))
                                      
                    #substract stopwords from tokens:

                    #for t in tokens:
                    #    if t not in stopWords:
                    #        vocabulary.append(t)
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
                            if left_context_word not in stopWords:

                                left_context.append(left_context_word)

                                # write context words in output file1:

                                output_writer1.writerow([fname, date_sent, "left", left_context_word])

                        # tokens[index_target_word+1:index_target_word+win_size+1] # this covers the right context of
                        # target_word

                        right_context_this_index = tokens[index_target_word+1:index_target_word+win_size+1] # this
                        # is the list of all words occurring in the right context of this occurrence of the target_word

                        # add the right context words of this occurrence of target_word (indexed by index_target_word)
                        # to right_context:

                        for right_context_word in right_context_this_index:
                            if right_context_word not in stopWords:
                                right_context.append(right_context_word)

                                # write context words in output file1:

                                output_writer1.writerow([fname, date_sent, "right", right_context_word])

                        # add left context words to the vocabulary:

                        for left_context_word in left_context:
                            if left_context_word not in stopWords:
                                vocabulary_list.append(left_context_word)
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
                            if right_context_word not in stopWords:
                                vocabulary_list.append(right_context_word)
                                if right_context_word in vocabulary:
                                    frequency = vocabulary[right_context_word] # this is the frequency of
                                    # right_context_word as counted so far
                                    frequency += 1 # add 1 to the frequency of left_context_word to account for this
                                    # occurrence of right_context_word with target_word
                                    vocabulary[right_context_word] = frequency
                                else:
                                    vocabulary[right_context_word] = 1

                    #print(vocabulary)
                    
                    #print("Letter_ID:", fname)
                    #print("left context words:", left_context)

                    #print("date:", date_sent)
                    
                    #check the date of the letter (date_sent) and see whether it is contained in t1 or t2
                    
                    #to do: if the date of the letter is contained in t1 then add context words to context_word_t1
                    # and if it's in t2 ,  add context words to context_word_t2:

                    if date_sent in time_period_1:
                        #print("the letter was written in t1")

                        # record frequency of left context words in t1 letters:

                        for left_context_word in left_context:
                            if left_context_word in context_words_t1:
                                frequency = context_words_t1[left_context_word]
                                frequency += 1
                                context_words_t1[left_context_word] = frequency
                            else:
                                context_words_t1[left_context_word] = 1

                        #print("context_words_t1:",context_words_t1)

                        # record frequency of right context words in t1 letters:

                        for right_context_word in left_context:
                            if right_context_word in context_words_t1:
                                frequency = context_words_t1[right_context_word]
                                frequency += 1
                                context_words_t1[right_context_word] = frequency
                            else:
                                context_words_t1[right_context_word] = 1


                    #else:
                        #print("the letter was not written in t1")

                        
                    if date_sent in time_period_2:
                        #print("the letter was written in t2")

                        # record frequency of left context words in t1 letters:

                        for left_context_word in left_context:
                            if left_context_word in context_words_t2:
                                frequency = context_words_t2[left_context_word]
                                frequency += 1
                                context_words_t2[left_context_word] = frequency
                            else:
                                context_words_t2[left_context_word] = 1

                        #print("context_words_t2:", context_words_t2)

                        # record frequency of right context words in t2 letters:

                        for right_context_word in left_context:
                            if right_context_word in context_words_t2:
                                frequency = context_words_t2[right_context_word]
                                frequency += 1
                                context_words_t2[right_context_word] = frequency
                            else:
                                context_words_t2[right_context_word] = 1

                    #else:
                        #print("the letter was not written in t2")

outfile1.close()
infile.close()

# define word vectors for target word in t1 and t2:
index = 0

vocabulary_list = list(set(vocabulary_list)) # I eliminate duplicates

for i in range(len(vocabulary_list)): # loop over all words in the vocabulary

    word = vocabulary_list[i]
    #print(word)
    # if the word appears in a context for target_word in t1:
    if word in context_words_t1:

        # add the frequency with which target_word occurs with word:
        target_word_t1.append(context_words_t1[word])

    else:
        # if word isn't a context word for target_word in t1, add 0:
        target_word_t1.append(0)

    if word in context_words_t2:
        # add the frequency with which target_word occurs with word:
        target_word_t2.append(context_words_t2[word])
    else:
        # if word isn't a context word for target_word in t2, add 0:
        target_word_t2.append(0)



# Open output2 file, which contains the vectors of target_word for t1 and t2:

outfile2 = open(outfile2_name, 'w+')

# print the list of all words in the vocabulary:

for word in vocabulary:

    outfile2.write(word + "\t")

outfile2.write("\n")

# print the list of all elements of the word vector for target_word in t1:

for context_word_t1 in target_word_t1:
    outfile2.write(str(context_word_t1) + "\t")

outfile2.write("\n")

# print the list of all elements of the word vector for target_word in t2:

for context_word_t2 in target_word_t2:
    outfile2.write(str(context_word_t2) + "\t")

outfile2.write("\n")

outfile2.close()

#calculate cosine distance between word vector for target_word in t1 and word vector for target_word in t2:
                    
cosine_distance = 1 - spatial.distance.cosine(target_word_t1, target_word_t2)
print('cosine_distance', str(cosine_distance))

# print cosine distance to third output file:

outfile3 = open(outfile3_name, 'w+')
outfile3.write(str(cosine_distance))
outfile3.close()
