#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:16:39 2018

@author: nt
"""

# Script for extracting keywords from Darwin's letters
# Author: Nicole Tamer


# Import libraries:

import os
import csv
from bs4 import BeautifulSoup

# Directory names and tag names:
folder = '/Users/nt/Documents/Darwin_project/Darwin_letters'
#tagnames = ['persName', 'date', 'keywords', 'abstract', 'text']

# List of files in input directory:
files = os.listdir(folder)
files = [f for f in files[:16000] if 'xml' in f]
#files = ["DCP-LETT-4166B.xml"]
# All the strings for output:
output_strs = []

# Open output file:
outfile = open('/Users/nt/Documents/Darwin_project/output/sender.csv', 'w+')
output_writer = csv.writer(outfile, delimiter = "\t")

# Write header row:
output_writer.writerow(["Letter_id", "Date_sent", "Sender", "Receiver"]) # TO DO: add more fields

# Open each file:
for fname in files:
    print(fname)
    with open(os.path.join(folder, fname), "r") as infile:
        file_data = []
        
        # Read the file:
        content = infile.read()
        
        # Initialize the fields required (sender, receiver, date_sent, keywords, abstract, letter_text):
        sender = ""
        receiver = ""
        date_sent = "" 
        
        soup = BeautifulSoup(content,'xml')
            
        corr_action = soup.find_all("correspAction")
        #print("sender_receiver=",sender_receiver) 
        for s in corr_action:
            
            if s.get('type') == "sent":
                sender = s.persName.get_text()
                print("sender:", sender)             
                
                                
            elif s.get('type') == "received":
                receiver = s.persName.get_text()
                print("receiver:", receiver)
               
        
        
        # Write fields to output file:fi
        output_writer.writerow([fname, date_sent, sender, receiver])
        

# close output file:
outfile.close()