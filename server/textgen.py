import markovify
import nltk
import re
import json

class POSifiedText(markovify.Text):

    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [word for word in words if word != '']
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

    def test_sentence_input(self, sentence):
        meaningful_word_count = 0
        valid_word_count = 0
        words = nltk.word_tokenize(sentence)
        pos_tokens = nltk.pos_tag(words)
        for token in pos_tokens:
            if self.filter_token(token) == True:
                meaningful_word_count += 1
            if not self.filter_token(token) == "neutral":
                valid_word_count += 1
        if valid_word_count > 0 and meaningful_word_count / valid_word_count > .6:
            return True
        else:
            return False

    def filter_token(self, token):
        '''Filter out tokens that are punctuation, linking verbs, have verbs, etc. that cannnot be filtered using NLTK's POS tagger.
        In theory the part-of-speech filter should eliminate all verbs, but things like quotation marks for (embedded) quotes can make it misclassify parts of speech'''
        word = token[0]
        pos = token[1]
        config = json.load(open("config.json"))
        punct_tokens = config['punct_tokens']
        articles = config["articles"]
        linking_verbs = config["linking_verbs"]
        aux_verbs = config["aux_verbs"]
        neutral_pos_filter = config["neutral_pos_filter"]
        exclude_pos_filter = config["exclude_pos_filter"]
        if word in punct_tokens or pos in neutral_pos_filter:
            return "neutral"
        if pos in exclude_pos_filter or word in punct_tokens or word.lower() in linking_verbs or word.lower() in aux_verbs or word.lower() in articles:
            return False
        else:
            return True


class TextGen:
    def __init__(self):
        self.markov_models = list()
        return

    def addMarkov(self, text, options):
        print("POSing")
        block_length = int(options['block_length'])
        if options['pos_markov']:
            self.markov_models.append(POSifiedText(text, state_size=block_length))
        else:
            self.markov_models.append(markovify.Text(text, state_size=block_length))

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