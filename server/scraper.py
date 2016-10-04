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
        if not validators.url(self.url):
            self.valid = False
            self.errorMsg = "not a URL"
            return self
        hostname = urlparse(self.url).hostname
        hostname = hostname[4:] if hostname[0:4] == "www." else hostname
        url_parts = urlsplit(self.url)
        if "gutenberg.org" in hostname:
            match = re.search("(?:files|ebooks|epub)\/(\d+)", url_parts.path)
            if match:
                self.source = "Gutenberg"
                self.document_id = int(match.group(1))
                author_set = get_metadata('author', self.document_id)
                self.author = list(author_set)[0] if len(author_set) else "Unknown"
                title_set = get_metadata("title", self.document_id)
                self.title = list(title_set)[0] if len(title_set) else "Unknown"
                self.valid = True
            else:
                self.valid = False
                self.errorMsg = "Problem processing URL"
        else:
            self.valid = False
            self.errorMsg = "Right now only Project Gutenberg is supported"
        return self

    def serialize(self):
        if not self.valid:
            return ***REMOVED***
                'valid': self.valid,
                'errorMsg': self.errorMsg
            ***REMOVED***
        else:
            return ***REMOVED***
                'valid' : self.valid,
                'source': self.source,
                'document_id': self.document_id,
                'author': self.author,
                'title': self.title
            ***REMOVED***