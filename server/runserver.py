from flask import Flask, request, jsonify
import json
from scraper import metadataScraper, textScraper
from textgen import TextGen
from pprint import pprint

app = Flask(__name__)

@app.route("/addGene", methods=['POST'])
def addGene():
    url = json.loads(request.get_data().decode(encoding='UTF-8'))
    scraper = metadataScraper(url)
    gene = scraper.serialize()
    return jsonify(gene)

@app.route("/mutate", methods=['POST'])
def mutate():
    options = json.loads(request.get_data().decode(encoding='UTF-8'))
    pprint(options)
    genes = options['genes']
    scraper = textScraper()
    textgen = TextGen()
    for gene in genes:
        gene = scraper.getText(gene)
        textgen.addMarkov(gene['text'], options)
    output = textgen.generateText()
    return output

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
