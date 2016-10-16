from flask import Flask, request, jsonify
import json
from scraper import metadataScraper, textScraper
from processor import Processor
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
    nlp = Processor()
    for gene in genes:
        gene = scraper.getText(gene)
        sentences_tokenized = nlp.tokenize_part_of_speech(gene['text'])
        nlp.filter_and_calculate(sentences_tokenized, .5)
    return ""

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
