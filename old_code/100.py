import os
from bs4 import BeautifulSoup

folder = '/Users/nt/Desktop/Darwin'
files = os.listdir(folder)
tagnames = ['persName', 'abstract', 'date', 'text']

files = [f for f in files[:10] if 'xml' in f]

output_strs = []

for fname in files:
    with open(os.path.join(folder, fname), "r") as infile:
        print("working on", fname)
        file_data= []
        content = infile.read()
        soup = BeautifulSoup(content,'xml')
        for tagname in tagnames:
            tag_data = soup.find(tagname)
            if tag_data is None:
                tag_text="MISSING"
            else:
                tag_text = tag_data.get_text()
            file_data.append(tag_text)

        output_strs.append("{}\t{}\n".format(fname, "\t".join(file_data).replace('\n', ' ')))

print(len(output_strs))
with open('/Users/nt/Desktop/10.csv', 'w') as outfile:
    outfile.writelines(output_strs)
print('yo dude im finito')