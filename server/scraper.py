import re
import validators
from urllib.parse import urlparse, urlsplit
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata

class Scraper:
    def __init__(self, url):
        self.url = url
        self.document_id = False
        self.errorMsg = False
        self.processUrl()
        return

    def processUrl(self):
        #Verify whether URL is valid and return Project Gutenberg metadata if URL is valid
        url_parts = urlsplit(self.url)
        match = re.search("(?:files|ebooks|epub)\/(\d+)", url_parts.path)
        self.source = "Project Gutenberg"
        self.document_id = int(match.group(1))
        author_set = get_metadata('author', self.document_id)
        self.author = list(author_set)[0] if len(author_set) else "Unknown"
        if ", " in self.author:
          #Reverse Last, First to First Last
          self.author = " ".join(self.author.split(", ")[::-1])
        title_set = get_metadata("title", self.document_id)
        self.title = list(title_set)[0] if len(title_set) else "Unknown"
        self.valid = True
        print(self.source)
        return self

    def serialize(self):
        return ***REMOVED***
            'source': self.source,
            'document_id': self.document_id,
            'author': self.author,
            'title': self.title
        ***REMOVED***
