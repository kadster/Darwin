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
files = [f for f in files [:] if 'xml' in f]

# All the strings for output:
output_strs = []

# Open output file:
outfile = open('/Users/nt/Documents/Darwin_project/output/fields.csv', 'w+')
output_writer = csv.writer(outfile, delimiter = "\t")

# Write header row:
output_writer.writerow(["Letter_id", "Date_sent", "Sender", "Receiver", "Keywords"]) # TO DO: add more fields

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
        date_sent = "" # the date in which the letter was sent
        keywords = "" # list of all keywords in the letter
        scientific_terms = []
        abstract = "" # summary of the letter
        letter_text = "" # transcription of the letter
        
        # Parse the XML of the file:
        soup = BeautifulSoup(content,'xml')
        
        # Extract sender, receiver, and date sent of the letter:

        
        corr_action = soup.find_all("correspAction")
        #print("sender_receiver=",sender_receiver) 
        for s in corr_action:
            
            if s.get('type') == "sent":
                sender = s.persName.get_text()
                print("sender:", sender)
                date_sent = s.date["when"]
                print("date sent:", date_sent)
                
            elif s.get('type') == "received":
                receiver = s.persName.get_text()
                print("receiver:", receiver)

  


# close output file:
outfile.close()
