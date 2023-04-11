import concurrent.futures
import os
import os.path as osp
import re
import urllib.request
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

HTTP_URL_PATTERN = r'^http[s]*://.+' # Regex pattern to match a URL
WEBSITE_DUMP_DIRECTORY = "text" # Directory to dump raw bs4 output
PROCESSED_CSV_DIRECTORY = "processed" # Directory to save processed CSV file
# ENTRY_POINTS = ["https://omscs.gatech.edu/",
#                 "https://www.gatech.edu/",
#                 "https://www.cc.gatech.edu/ms-computer-science-admissions-faq",
#                 "https://housing.gatech.edu/",
#                 "https://hr.gatech.edu/",
#                 "https://health.gatech.edu/student-health-insurance/",
#                 "https://cse.gatech.edu/",
#                 "https://support.cc.gatech.edu/services/web-hosting",
#                 "https://webmasters.gatech.edu/handbook/guide-domain-names",
#                 "https://catalog.gatech.edu/coursesaz/",
#                 "https://catalog.gatech.edu/courses-grad/",
#                 "https://www.gatech.edu/academics/all-degree-programs",
#                 ] # Define website entry points
ENTRY_POINTS = []

# Create a class to parse the HTML and get the hyperlinks
class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        # Create a list to store the hyperlinks
        self.hyperlinks = []

    # Override the HTMLParser's handle_starttag method to get the hyperlinks
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # If the tag is an anchor tag and it has an href attribute, add the href attribute to the list of hyperlinks
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

# Function to get the hyperlinks from a URL


def get_hyperlinks(url):

    # Try to open the URL and read the HTML
    try:
        # Open the URL and read the HTML
        with urllib.request.urlopen(url) as response:

            # If the response is not HTML, return an empty list
            if not response.info().get('Content-Type').startswith("text/html"):
                return []

            # Decode the HTML
            html = response.read().decode('utf-8')
    except Exception as e:
        print(e)
        return []

    # Create the HTML Parser and then Parse the HTML to get hyperlinks
    parser = HyperlinkParser()
    parser.feed(html)

    return parser.hyperlinks

# Function to get the hyperlinks from a URL that are within the same domain


def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        # If the link is a URL, check if it is within the same domain
        if re.search(HTTP_URL_PATTERN, link):
            # Parse the URL and check if the domain is the same
            url_obj = urlparse(link)
            if local_domain in url_obj.netloc:
                clean_link = link

        # If the link is not a URL, check if it is a relative link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:") or link.startswith('java') or link.startswith('tel'):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    # Return the list of hyperlinks that are within the same domain
    return list(set(clean_links))


def remove_duplicate_newlines(s):
    return re.sub(r'(\n)+', r'\n', s)


def scrape_page(url: str):
    print(url)  # for debugging and to see the progress

    # Get local domain
    local_domain = urlparse(url).netloc

    # Get the text from the URL using BeautifulSoup
    try:
        resp = requests.get(url, timeout=1000, verify=False)
        if resp.status_code != 200:
            return

        if not resp.headers['Content-Type'].startswith("text/html"):
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        # Get the text but remove the tags
        text = soup.get_text()
        text = remove_duplicate_newlines(text)

        if text.startswith("Page Not Found"):
            return

    # If the crawler gets to a page that requires JavaScript, it will stop the crawl
        if "You need to enable JavaScript to run this app." in text or "requires JavaScript to be enabled" in text:
            print("Unable to parse page " + url +
                  " due to JavaScript being required")

    # Otherwise, write the text to the file in the 'text' directory
        # Create text/<local_domain> directory for HTML dump
        sub_directory = osp.join(WEBSITE_DUMP_DIRECTORY, local_domain)
        if not os.path.exists(sub_directory):
            os.mkdir(sub_directory)
        # Save text from the url to a <url>.txt file
        file_name = url[8:].replace("/", "*") + ".txt"
        with open(osp.join(sub_directory, file_name), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print("err" + " " + e + " " + url)

    return get_domain_hyperlinks(local_domain, url)


def crawl(urls):
    # Create a queue to store the URLs to crawl
    queue = urls

    # Create a set to store the URLs that have already been seen (no duplicates)
    seen = set(urls)

    # Create a directory to store the text files
    if not os.path.exists(WEBSITE_DUMP_DIRECTORY):
        os.mkdir(WEBSITE_DUMP_DIRECTORY)

    # While the queue is not empty, continue crawling
    with concurrent.futures.ThreadPoolExecutor() as excutor:
        while queue:
            futures = [excutor.submit(scrape_page, url) for url in queue]
            queue = []
            try:
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()

                    if not res:
                        continue

                    for url in res:
                        if url not in seen:
                            seen.add(url)
                            queue.append(url)
            except Exception as e:
                print(e)


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def to_csv():
    # Create a directory to store the csv files
    if not os.path.exists(PROCESSED_CSV_DIRECTORY):
        os.mkdir(PROCESSED_CSV_DIRECTORY)
    texts = []
    total_words = 0
    seen_texts = set() # avoid duplicates
    for domain in os.listdir(WEBSITE_DUMP_DIRECTORY):
        domain_dump = osp.join(WEBSITE_DUMP_DIRECTORY, domain)
        for fname in os.listdir(domain_dump):
            site_dump = osp.join(WEBSITE_DUMP_DIRECTORY, domain, fname)
            site_url = fname[:-4].replace("*", "/") # remove .txt at the end and restore '/'
            if not site_url.startswith(domain):
                site_url = domain[0] + site_url
            with open(site_dump, "r", encoding="UTF-8") as f:
                text = f.read()
                text_len = len(text.split())
                # ignore pages with more than 10,000 words (mainly archives)
                if text_len > 1e4: continue
                if text not in seen_texts:
                    texts.append((site_url, text))
                    total_words += text_len
                seen_texts.add(text)


    df = pd.DataFrame(texts, columns=['url', 'text'])
    df['text'] = remove_newlines(df.text)
    df.to_csv('processed/scraped.csv')
    print(df.head())
    print(f'Total websites: {len(df)}')
    print(f'Total words: {total_words}')
    print(f'Estimated embedding cost: ${total_words / 0.75 / 1000 * 0.0004:.2f}')

def initialize():
    for domain in os.listdir(WEBSITE_DUMP_DIRECTORY):
        for fname in os.listdir(osp.join(WEBSITE_DUMP_DIRECTORY, domain)):
            url = 'https://' + fname[:-4].replace('*', '/')
            ENTRY_POINTS.append(url)
    print(f'Initialized with {len(ENTRY_POINTS)} URLs')

if __name__ == "__main__":
    #initialize()
    #crawl(ENTRY_POINTS)
    print("convert to csv....")
    to_csv()
