import os
from bs4 import BeautifulSoup

folder = '/Users/nt/Documents/Darwin_project/Darwin_letters'
files = os.listdir(folder)

# print(files)
files = [f for f in files if 'xml' in f] # find all files which are only xml format

output_strs = [] # [] defines mutable data types - lists, list comprehensions and for indexing/lookup/slicing
for fname in files:
    with open(os.path.join(folder, fname), "r") as infile:
        #print(fname)
        content = infile.read()
        soup = BeautifulSoup(content,'xml')
        persName = soup.find_all('persName') # change tag depending on what you want to get

        for fname in files:
            text = persName.get_text()
            output_strs.append("{}\t{}\n".format(fname, text.replace('\n', ' ')))
            
print(quote.text.encode('utf-8'))

print(len(output_strs)) #returns length of output_strs
with open('/Users/nt/Desktop/persName_abstract.dat', 'w') as outfile:
    outfile.writelines(output_strs)

