import markovify
import nltk
import json
from markovify.chain import Chain

class TextGen:
    def __init__(self):
        self.markov_models = list()
        return

    def addMarkov(self, text, options):
        print("adding Markov")
        ngram_size = int(options['ngram_size'])
        self.markov_models.append(markovify.Text(text, state_size=ngram_size))

    def generateText(self):
        output = "    "
        if len(self.markov_models) > 1:
            textgen = markovify.combine(self.markov_models)
        else:
            textgen = self.markov_models[0]
        sentence_count = 0
        while sentence_count <= 12:
            sentence = textgen.make_sentence()
            if isinstance(sentence, str):
                output += " " + sentence
                sentence_count += 1
                if sentence_count % 4 == 0:
                    print(sentence)
                    output += "\n\n"
        return output
