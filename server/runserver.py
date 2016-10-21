from flask import Flask, request, jsonify
import json
from scraper import Gene, getText
from textgen import TextGen
from pprint import pprint

app = Flask(__name__)

@app.route("/addGene", methods=['POST'])
def addGene():
    url = json.loads(request.get_data().decode(encoding='UTF-8'))
    scraper = Gene(url)
    gene = scraper.as_dict()
    return jsonify(gene)

@app.route("/mutate", methods=['POST'])
def mutate():
    options = json.loads(request.get_data().decode(encoding='UTF-8'))
    pprint(options)
    genes = options['genes']
    textgen = TextGen()
    for gene in genes:
        text = getText(gene)
        textgen.addMarkov(text, options)
    output = textgen.generateText()
    return output

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
