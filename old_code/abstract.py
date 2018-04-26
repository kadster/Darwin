import os
from bs4 import BeautifulSoup

folder = '/Users/nt/Desktop/letters'
files = os.listdir(folder)

# print(files)
files = [f for f in files if 'xml' in f] # find all files which are only xml format

output_strs = [] # [] defines mutable data types - lists, list comprehensions and for indexing/lookup/slicing
for fname in files:
    with open(os.path.join(folder, fname), "r") as infile:
        #print(fname)
        content = infile.read()
        BeautifulSoup(markup, "lxml-xml")
        soup = BeautifulSoup(content,'xml')
        persNames = soup.find_all('persName') # change tag depending on what you want to get
        #write all the abstracts to the output_strs
        #\t for "tab"
        #\n for "newline"
        #replace "newline" with spaces
        for persName in persNames:
            text = persName.get_text()
            output_strs.append("{}\t{}\n".format(fname, text.replace('\n', ' ')))

print(len(output_strs)) #returns length of output_strs
with open('/Users/nt/Desktop/persname.dat', 'w') as outfile:
    outfile.writelines(output_strs)
print('yo dude im finito')
