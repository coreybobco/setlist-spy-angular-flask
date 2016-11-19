from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
import random
import re
from urllib.parse import urlparse, urlsplit
from io import StringIO
import sys
from gene import Gene

class GutenbergScraper(Gene):
    def __init__(self, url):
        self.source = "Project Gutenberg"
        self.url = url
        self.document_id = False
        self.fetch_metadata()
        return

    def fetch_metadata(self):
        if self.url == "random":
            language = False
            while language != "en":
                self.document_id = random.randint(1, 53273) #Pick book at random (max id is currently 53273)
                language_set = get_metadata('language', self.document_id)
                language = list(language_set)[0] if len(language_set) else False
            self.url = "http://www.gutenberg.org/ebooks/" + str(self.document_id)
        else:
            #Get Project Gutenberg document ID from url string
            url_parts = urlsplit(self.url)
            match = re.search("(?:files|ebooks|epub)\/(\d+)", url_parts.path)
            self.document_id = int(match.group(1))
        author_set = get_metadata('author', self.document_id)
        self.author = list(author_set)[0] if len(author_set) else "Unknown"
        if ", " in self.author:
          #Reverse Last, First to First Last
          self.author = " ".join(self.author.split(", ")[::-1])
        title_set = get_metadata("title", self.document_id)
        self.title = list(title_set)[0] if len(title_set) else "Unknown"
        return self
