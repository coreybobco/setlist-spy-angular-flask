from capturer import CaptureOutput
from gutenberg.acquire import load_etext
from internetarchive import download
import requests

class Gene:
    def __init__(self, url):
        return

    def as_dict(self):
        return ***REMOVED***
            'document_id': self.document_id,
            'title': self.title,
            'author': self.author,
            'source': self.source,
            'url': self.url
        ***REMOVED***

def get_text(gene):
    if gene['source'] == "Project Gutenberg":
        text = strip_headers(load_etext(gene['document_id']).strip())
    elif gene['source'] == "Archive.org":
        with CaptureOutput() as capturer:
            download(gene['document_id'], glob_pattern="*txt", dry_run=True)
        url = capturer.get_text()
        text = requests.get(url).text
    return text
