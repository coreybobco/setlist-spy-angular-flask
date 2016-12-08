#!/usr/bin/env python3
from flask import Flask, request
import json
from setlistspy.mixesdb import MixesDBScraper

app = Flask(__name__)

@app.route("/setlistSearch", methods=['POST'])
def setlist_search():
    search_input = json.loads(request.get_data().decode(encoding='UTF-8'))
    search_input = " ".join(search_input.split()) #Normalize whitespace
    mdb = MixesDBScraper()
    set_urls = mdb.get_set_urls(search_input)
    tracklist = mdb.get_tracklist(set_urls)
    return json.dumps(tracklist)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
