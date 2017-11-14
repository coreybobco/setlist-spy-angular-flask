#!/usr/bin/env python3
from flask import Flask, request
import json
from search import Search
from pprint import pprint

app = Flask(__name__)

@app.route("/setlistSearch", methods=['POST'])
def setlist_search():
    search_input = json.loads(request.get_data().decode(encoding='UTF-8'))
    search_input = " ".join(search_input.split()) #Normalize whitespace
    search = Search(search_input)
    pprint(search.results)
    return json.dumps(search.results)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=4100,
        debug=True
    )
