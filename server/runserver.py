#!/usr/bin/env python3
from flask import Flask, request, jsonify, Response
import json
from pprint import pprint
from urllib.parse import urlsplit
from mutagen.archive import ArchiveScraper
from mutagen.gutenberg import GutenbergScraper
from mutagen.gene import get_text
from mutagen.textgen import TextGen
from setlistspy.mixesdb import MixesDBScraper

app = Flask(__name__)

@app.route("/setlistSearch", methods=['POST'])
def setlist_search():
    DJ = json.loads(request.get_data().decode(encoding='UTF-8'))
    DJ = " ".join(DJ.split()) #Normalize whitespace
    mdb = MixesDBScraper(DJ)
    tracklist = list(mdb.tracklist)
    tracklist.sort()
    return json.dumps(tracklist)

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
