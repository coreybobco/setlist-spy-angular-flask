import re
import validators
from urllib.parse import urlparse, urlsplit
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
import random

class metadataScraper:
    def __init__(self, url):
        self.source = "Project Gutenberg"
        self.url = url
        self.document_id = False
        self.errorMsg = False
        self.processUrl()
        return

    def processUrl(self):
        #Verify whether URL is valid and return Project Gutenberg metadata if URL is valid
        print(self.url)
        if self.url == "random":
            self.document_id = random.randint(1, 53273) #Pick book at random (max id is currently 53273)
        else:
            url_parts = urlsplit(self.url)
            match = re.search("(?:files|ebooks|epub)\/(\d+)", url_parts.path)
            self.document_id = int(match.group(1))
        print(self.document_id)
        author_set = get_metadata('author', self.document_id)
        self.author = list(author_set)[0] if len(author_set) else "Unknown"
        if ", " in self.author:
          #Reverse Last, First to First Last
          self.author = " ".join(self.author.split(", ")[::-1])
        title_set = get_metadata("title", self.document_id)
        self.title = list(title_set)[0] if len(title_set) else "Unknown"
        self.valid = True
        return self

    def serialize(self):
        return ***REMOVED***
            'source': self.source,
            'document_id': self.document_id,
            'author': self.author,
            'title': self.title
        ***REMOVED***

class textScraper():
    def __init__(self):
        return

    def getText(self, gene):
        if gene['source'] == "Project Gutenberg":
            gene['text'] = strip_headers(load_etext(gene['document_id']).strip())
        return gene
