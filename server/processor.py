import json
import nltk
from pprint import pprint
from collections import OrderedDict

class Processor:
	def __init__(self):
		self.config = json.load(open("config.json"))
		return

	def tokenize_part_of_speech(self, text):
		sentences = nltk.sent_tokenize(text)
		sentences_tokenized = OrderedDict()
		for sentence in sentences:
			words = nltk.word_tokenize(sentence)
			sentences_tokenized[sentence] = nltk.pos_tag(words)
		return sentences_tokenized

	def filter_and_calculate(self, sentences_tokenized, target_ratio):
		# Calculate ratio of filtered parts of speech
		garbage_sentences = 0
		for sentence, pos_tokens in sentences_tokenized.items():
			meaningful_word_count = 0
			valid_word_count = 0
			token_count = len(pos_tokens)
			for token in pos_tokens:
				if self.filter_token(token) == True:
					meaningful_word_count += 1
				if not self.filter_token(token) == "neutral":
					valid_word_count += 1
			sentence_ratio = meaningful_word_count / valid_word_count
			if sentence_ratio <= target_ratio:
				garbage_sentences += 1
				print(sentence)
				print(str(meaningful_word_count) + " meaningful words / " + str(valid_word_count) + " valid words. " + str(token_count) + " tokens\n")
		print(str(garbage_sentences) + " out of " + str(len(sentences_tokenized)) + " sentences.")
		return ""

	def filter_token(self, token):
		'''Filter out tokens that are punctuation, linking verbs, have verbs, etc. that cannnot be filtered using NLTK's POS tagger.
		In theory the part-of-speech filter should eliminate all verbs, but things like quotation marks for (embedded) quotes can make it misclassify parts of speech'''
		word = token[0]
		pos = token[1]
		punct_tokens = self.config['punct_tokens']
		articles = self.config["articles"]
		linking_verbs = self.config["linking_verbs"]
		aux_verbs = self.config["aux_verbs"]
		neutral_pos_filter = self.config["neutral_pos_filter"]
		exclude_pos_filter = self.config["exclude_pos_filter"]
		if word in punct_tokens or pos in neutral_pos_filter:
			return "neutral"
		if pos in exclude_pos_filter or word in punct_tokens or word.lower() in linking_verbs or word.lower() in aux_verbs or word.lower() in articles:
			return False
		else:
			return True
