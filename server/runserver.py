from flask import Flask, request, jsonify
import json
from scraper import metadataScraper, textScraper
from processor import Processor
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
    genes = json.loads(request.get_data().decode(encoding='UTF-8'))
    scraper = textScraper()
    target_ratio = .6
    textgen = TextGen()
    for gene in genes:
        nlp = Processor(target_ratio)
        gene = scraper.getText(gene)
        # nlp.filter_and_purge(gene['text'])
        textgen.addMarkov(gene['text'])
        # textgen.addMarkov(nlp.filtered_text)
    output = textgen.generateText()
    return output

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
