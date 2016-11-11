import markovify
import nltk
from spacy.en import language_data
import json
from markovify.chain import Chain

class MutagenText(markovify.Text):
    def __init__(self, input_text, state_size=2, filter_stopwords_ratio=False, chain=None):
        """
        input_text: A string.
        state_size: An integer, indicating the number of words in the model's state.
        chain: A trained markovify.Chain instance for this text, if pre-processed.
        """
        self.input_text = input_text
        self.state_size = state_size
        self.filter_stopwords_ratio = float(filter_stopwords_ratio) if filter_stopwords_ratio else False
        runs = list(self.generate_corpus(input_text))
        # Rejoined text lets us assess the novelty of generated setences
        self.rejoined_text = self.sentence_join(map(self.word_join, runs))
        self.chain = chain or Chain(runs, state_size)

    def test_sentence_input(self, sentence):
        if super(MutagenText, self).test_sentence_input(sentence):
            if self.filter_stopwords_ratio:
                meaningful_word_count = 0
                words = nltk.word_tokenize(sentence)
                stopwords = set(language_data.STOP_WORDS)
                for word in words:
                    if not word in stopwords:
                        meaningful_word_count += 1
                if len(words) and meaningful_word_count / len(words) > self.filter_stopwords_ratio:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

class TextGen:
    def __init__(self):
        self.markov_models = list()
        return

    def addMarkov(self, text, options):
        print("adding Markov")
        block_length = int(options['block_length'])
        filter_stopwords_ratio = float(options['purge_ratio'])
        if options['purge_mode']:
            self.markov_models.append(MutagenText(text, block_length, filter_stopwords_ratio))
        else:
            self.markov_models.append(markovify.Text(text, state_size=block_length))
        print("yo")

    def generateText(self):
        output = "    "
        if len(self.markov_models) > 1:
            textgen = markovify.combine(self.markov_models)
        else:
            textgen = self.markov_models[0]
        for i in range(500):
            sentence = textgen.make_sentence()
            if isinstance(sentence, str):
                output += " " + sentence
        return output
