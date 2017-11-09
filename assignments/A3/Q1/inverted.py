import io
import os
import sys
import html2text
from tabulate import tabulate
from bs4 import BeautifulSoup

file_names = set()
for root, dirs, files in os.walk(os.path.abspath('./en')):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            file_names.add(filepath)

index = {}
all_words = set()
for file_name in file_names:
    try:
        h = html2text.HTML2Text()
        h.ignore_links = True
        text = h.handle(u' '.join([line.strip() for line in io.open(file_name, "r", encoding="utf-8").readlines()]))
        words = [word.lower() for word in text.split() if word.isalpha()]
        all_words |= set(words)
        index[file_name.split(os.pathsep)[-1]] = words
    except:
        pass

inverted_index = {}
for word in all_words:
    files = []
    for file, words in index.items():
        if word in words:
            files.append(file)
    inverted_index[word] = sorted(set(files))

inverted_index_table = []
for word in inverted_index:
    try:
        inverted_index_table.append([word, u', '.join(inverted_index[word])])
    except:
        pass

#print tabulate(inverted_index_table, headers=["Word", "Documents"])
output = open("output.txt", "w")
output.write(tabulate(inverted_index_table, headers=["Word", "Documents"]))
output.close()