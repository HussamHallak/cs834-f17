import os
import sys
import io
import html2text
from bs4 import BeautifulSoup
from tabulate import tabulate



print "Processing files..."
for file in html_files:
    try:
        soup = BeautifulSoup(open(file), 'html.parser')
        anchors = soup.find_all('a', href=True)
        for a in anchors:
            link = a['href']
            text = a.string or ''
            if not link.startswith('http'):
                try:
                    link = os.path.join(os.path.dirname(file), link)
                    link = os.path.abspath(link)
                except:
                    pass
            all_links.setdefault(file, [])
            all_anchor_text.setdefault(file, [])
            if file != link and link not in all_links[file] and os.path.isfile(link):
                all_links[file].append(link)
                all_anchor_text[file].append(text)
    except:
        pass

print "Finding links' frequencies..."
link_frequency = {}
link_text = {}
for source in all_links:
    destinations = all_links[source]
    texts = all_anchor_text[source]

    for index, destination in enumerate (destinations):
        link_frequency.setdefault(destination, 0)
        link_frequency[destination] += 1
        link_text.setdefault(destination, [])
        link_text[destination].append(texts[index])

link_frequency_table = []
for link in link_frequency:
    link_frequency_table.append([link, link_frequency[link]])
link_frequency_table = sorted(link_frequency_table, key=lambda x:x[1], reverse=True)
anchor_link_frequency_table = []
for row in link_frequency_table:
    row += [u', '.join(set(link_text[row[0]]))]
    row[0] = os.path.basename(row[0])
    anchor_link_frequency_table.append(row)
link_frequency_table = anchor_link_frequency_table
link_frequency_table = link_frequency_table[:10]

print "Writing the results to output file..."
output = open("output.txt", "w")
output.write(tabulate(link_frequency_table, headers=["File", "Number of inlinks", "Anchor text(s)"]))
output.close()
print "Done!"