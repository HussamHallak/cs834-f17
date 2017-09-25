import sys
import time
from bs4 import *
import urllib2
import re

def crawl(url):
    url = url.strip()
    page_file_name = str(hash(url))
    page_file_name = page_file_name + ".html"
    fh_page = open(page_file_name, "w")
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    html_text = str(soup)
    fh_page.write(url + "\n")
    fh_page.write(page_file_name + "\n")
    fh_page.write(html_text)
    fh_page.close()
    children_links = set()
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        children_links.add(link.get('href'))

    #convert relative links to absolute links
    for child in children_links:
        if isAbsolute(child):
            new_child = urllib2.urlparse.urljoin(url, child)
            children_links.remove(child)
            children_links.add(new_child)

    links_to_return = set()
    for child in children_links:
        try:
            r = urllib2.urlopen(child)
            http_message = r.info()
            full = http_message.type
            if full == "text/html" and r.getcode() == 200:
                links_to_return.add(child)
        except urllib2.HTTPError as e:
            print "There is an error crawling links in this page:"
            print "Error Code:"
            print e.code

    return links_to_return


def isAbsolute(url):
    try:
        return bool(urlparse(url).netloc)
    except:
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
	print "Usage: python crawl.py <seed_url> <pages_count>"
	print "e.g: python crawl.py https://www.yahoo.com/ 20"
	exit()
    url = sys.argv[1]
    pages_count = int(sys.argv[2])
    print "Entered URL:"
    print url
    html_page = urllib2.urlopen(url)
    print "Final URL:"
    print html_page.geturl()
    print "*******************"
    links_to_crawl = set()
    links_to_crawl.add(html_page.geturl())
    found_links = set()
    crawled_links = set()
    counter = 0
    while links_to_crawl and counter < pages_count:
        link = links_to_crawl.pop()
        print "crawling: " + link
        new_links = crawl(link)
        crawled_links.add(link)
        for new_link in new_links:
            if new_link not in crawled_links:
                links_to_crawl.add(new_link)
            if new_link not in found_links:
                print "New link found: " + new_link
                found_links.add(new_link)
        time.sleep(5)
        counter += 1