'''
Simple program to gather all the internal and external links. NOT to be confused with inlinks and outlinks.
Internal links are those links that point to another website within the same domain
External links are those links that point to another website that does NOT share the same domain
Reference link: https://www.thepythoncode.com/article/extract-all-website-links-python
'''

# First step is to import all the basic libraries required. 
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import pandas as pd
import numpy as np
import time

#Colorama is a simple tool used to display different colors on the terminal 
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# max_urls define the maximum number of urls it must crawl to obtain the rest of the urls
# The internal and external URLs are put into sets to prevent redundancy
max_urls = 10
internal_urls = set()
external_urls = set()

#Basic methos to find whether a given URL is valid or not, just like our method
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Below function gets all the links, and as a trial we consider only the a tags for the time being.     
def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

total_urls_visited = 0

def crawl(url, max_urls):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 10.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

Sample1 = pd.read_csv('whoisLegi.csv').sample(10)

start = time.time()
count = 1
print("Program starting, for any URLs taking more than 10s press ctrl+c")
for i in Sample1.URL:
    print("URL:",count)
    count +=1
    try:
        crawl(i, max_urls)
        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total External links:", len(external_urls))
        print("[+] Total URLs:", len(external_urls) + len(internal_urls))
        print("[+] Total crawled URLs:", max_urls)
    except:
        print("Not a valid URL\n")
        continue
end = time.time()
print("Finished execution in:",end-start,"seconds")
















