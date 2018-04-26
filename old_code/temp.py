# Import libraries:

import os
from bs4 import BeautifulSoup

# Directory names and tag names:
folder = '/Users/nt/Documents/Darwin_letters'
tagnames = ['date']

# List of files in input directory:
files = os.listdir(folder)
files = [f for f in files[:] if 'xml' in f]

# All the strings for output:
output_strs = []

# Open each file:
for fname in files:
    with open(os.path.join(folder, fname), "r") as infile:
        file_data = []
        
        # Read the file:
        content = infile.read()
        
        # Parse the XML of the file:
        soup = BeautifulSoup(content,'xml')
        
        # Extract content of tagname in file:
        
        for tagname in tagnames:
            tag_data = soup.find(tagname)
            if tag_data is None:
                tag_text="MISSING"
            else:
                # Extract the scientific keywords in the letters:
                if tagname == "keywords":
                    transcription = soup.find(type="scientific_terms")
                    temp = tag_data.get_text()
                    if transcription is not None:
                        tag_text="scientific"
                    else:
                        tag_text = tag_data.get_text()
                        if tag_text is not soup.find(type="scientific_terms"):
                            tag_text="not scientific"

            file_data.append(',\"' + tag_text + '\"')

        output_strs.append("{}\t{}\n".format(fname, "\t".join(file_data).replace('\n', ' ')))


print(len(output_strs))
with open('/Users/nt/Desktop/keywords.csv', 'w+') as outfile:
    outfile.writelines(output_strs)
