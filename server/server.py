from flask import Flask, request, jsonify
import json
from scraper import Scraper
from pprint import pprint

app = Flask(__name__)

@app.route("/addBook", methods=['POST'])
def addBook():
    url = json.loads(request.get_data().decode(encoding='UTF-8'))
    print(url)
    bookScraper = Scraper(url)
    book_info = bookScraper.serialize()
    return jsonify(book_info)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=9000,
        debug=True
    )
