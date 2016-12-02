from internetarchive import get_item, download
from lxml import html
import requests
import random
import re
from urllib.parse import urlsplit
from mutagen.gene import Gene

class ArchiveScraper(Gene):
    def __init__(self, url):
        self.source = "Archive.org"
        self.url = url
        self.document_id = False
        # getText()
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
            #Get Archive.org unique identifier from url string
            url_parts = urlsplit(self.url)
            url_path_parts = url_parts.path.split("/")
            if len(url_path_parts) > 2:
                self.document_id = url_path_parts[2]
        item = get_item(self.document_id)
        if item:
            self.author = item.item_metadata['metadata'].get("author", "Unknown")
            if ", " in self.author:
                self.author = " ".join(self.author.split(", ")[::-1])
            self.title = item.item_metadata['metadata'].get("title", "Unknown")
        return self
