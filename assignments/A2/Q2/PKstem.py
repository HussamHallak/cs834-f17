import sys
import os
import io
import html2text
from nltk import PorterStemmer
import krovetzstemmer
if __name__ == "__main__":
    if len(sys.argv) < 2:
	print "Usage: python PKstem.py <file1> <file2> <file3> ..."
	print "e.g: python PKstem.py index.html myPage.html default.html some_page.html"
	exit()
file_names = set()
for i in range(1,len(sys.argv)):
	file_names.add(sys.argv[i])
porter = PorterStemmer()
krovetz = krovetzstemmer.Stemmer()
output = {}
for file_name in file_names:
    print "Stemming: " + file_name
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(u' '.join([line.strip() for line in io.open(file_name, "r", encoding="utf-8").readlines()]))
    words = set()
    for word in text.split():
        if word.isalpha():
            words.add(word.lower())
    words = sorted(words)
    porter_output = set()
    krovetz_output = set()
    for word in words:
        porter_output.add(porter.stem(word))
        krovetz_output.add(krovetz.stem(word))
    porter_output = sorted(porter_output)
    krovetz_output = sorted(krovetz_output )
    output[file_name] = {}
    output[file_name]['original_text'] = u' '.join(words)
    output[file_name]['porter'] = u' '.join(porter_output)
    output[file_name]['krovetz'] = u' '.join(krovetz_output)
print "Unique words in the original text:"
print "------------------------------------"
print output[file_name]['original_text']
print "Unique stems from Porter stemmer:"
print "------------------------------------"
print output[file_name]['porter']
print "Unique stems from Krovetz stemmer:"
print "------------------------------------"
print output[file_name]['krovetz']
print "The number of unique words in the original text:"
print "---------------------------------------------------"
print len(set(output[file_name]['original_text'].split()))
print "The number of unique stems from Porter stemmer:"
print "---------------------------------------------------"
print len(set(output[file_name]['porter'].split()))
print "The number of unique stems from Krovetz stemmer:"
print "---------------------------------------------------"
print len(set(output[file_name]['krovetz'].split()))