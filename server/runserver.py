#!/usr/bin/env python3
from flask import Flask, request, jsonify, Response
import json
from setlistspy.mixesdb import MixesDBScraper

app = Flask(__name__)

@app.route("/setlistSearch", methods=['POST'])
def setlist_search():
    DJ = json.loads(request.get_data().decode(encoding='UTF-8'))
    DJ = " ".join(DJ.split()) #Normalize whitespace
    mdb = MixesDBScraper()
    set_urls = mdb.get_set_urls(DJ)
    tracklist = mdb.get_tracklist(set_urls)
    return json.dumps(tracklist)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
