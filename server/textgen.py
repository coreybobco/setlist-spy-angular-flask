import markovify

class TextGen:
    def __init__(self):
        self.markov_models = list()
        return

    def addMarkov(self, text):
        self.markov_models.append(markovify.Text(text))

    def generateText(self):
        output = ""
        if len(self.markov_models) > 1:
            textgen = markovify.combine(self.markov_models)
        else:
            textgen = self.markov_models[0]
        for i in range(500):
            sentence = textgen.make_sentence()
            if isinstance(sentence, str):
                output += " " + sentence
        return output