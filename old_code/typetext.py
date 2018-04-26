import os
from bs4 import BeautifulSoup

folder = '/Users/nt/Desktop/Darwin'
files = os.listdir(folder)
tagnames = ['persName', 'date', 'keywords', 'abstract', 'text']

files = [f for f in files[:20] if 'xml' in f]

output_strs = []

for fname in files:
    with open(os.path.join(folder, fname), "r") as infile:
        file_data = []
        content = infile.read()
        soup = BeautifulSoup(content,'xml')

        for tagname in tagnames:
            tag_data = soup.find(tagname)
            if tag_data is None:
                tag_text="MISSING"
            else:
                transcription = soup.find(type="transcription")
                if transcription is not None:
                    tag_text = transcription.get_text()
                else:
                    tag_text = tag_data.get_text()
                    if tag_text is "":
                        tag_text="TRANSCRIPTION MISSING"

            file_data.append(",\"" + tag_text + "\"")



        output_strs.append("{}\t{}\n".format(fname, "\t".join(file_data).replace('\n', ' ')))


print(len(output_strs))
with open('/Users/nt/Desktop/text2.csv', 'w') as outfile:
    outfile.writelines(output_strs)
print('yo dude im finito')
