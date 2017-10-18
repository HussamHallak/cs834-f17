import io
import os
import sys
import html2text
from tabulate import tabulate

if __name__ == "__main__":
    if len(sys.argv) < 2:
	print "Usage: python inverted.py <file1> <file2> <file3> ..."
	print "e.g: python inverted.py index.html myPage.html default.html some_page.html"
	exit()

file_names = set()
for i in range(1,len(sys.argv)):
	file_names.add(sys.argv[i])

index = {}
all_words = set()
for file_name in file_names:
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(u' '.join([line.strip() for line in io.open(file_name, "r", encoding="utf-8").readlines()]))
    words = [word.lower() for word in text.split() if word.isalpha()]
    all_words |= set(words)
    index[file_name.split(os.pathsep)[-1]] = words

inverted_index = {}
for word in all_words:
    files = []
    for file, words in index.items():
        if word in words:
            files.append(file)
    inverted_index[word] = sorted(set(files))

inverted_index_table = []
for word in inverted_index:
    inverted_index_table.append([word, u', '.join(inverted_index[word])])

print tabulate(inverted_index_table, headers=["Word", "Documents"])
output = open("output.txt", "w")
output.write(tabulate(inverted_index_table, headers=["Word", "Documents"]))
output.close()