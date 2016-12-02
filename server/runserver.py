#!/usr/bin/env python3
from flask import Flask, request, jsonify
import json
from pprint import pprint
from archive_scraper import ArchiveScraper
from gutenberg_scraper import GutenbergScraper
from gene import get_text
from urllib.parse import urlsplit
from textgen import TextGen

app = Flask(__name__)

@app.route("/setlistSearch", methods=['POST'])
def setlist_search():
    DJ = json.loads(request.get_data().decode(encoding='UTF-8'))
    print(DJ)
    return ''

@app.route("/addGene", methods=['POST'])
def addGene():
    print('working')
    url = json.loads(request.get_data().decode(encoding='UTF-8'))
    hostname = urlsplit(url).netloc
    if hostname.startswith("www."):
        hostname = hostname[4::]
    if hostname == "archive.org":
        scraper = ArchiveScraper(url)
    else:
        scraper = GutenbergScraper(url)
    gene = scraper.as_dict()
    return jsonify(gene)

@app.route("/mutate", methods=['POST'])
def mutate():
    options = json.loads(request.get_data().decode(encoding='UTF-8'))
    genes = options['genes']
    textgen = TextGen()
    for gene in genes:
        text = get_text(gene)
        textgen.addMarkov(text, options)
    output = textgen.generateText()
    return output

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
