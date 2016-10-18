import json
import nltk
from pprint import pprint
from collections import OrderedDict

class Processor:
	def __init__(self, target_ratio):
		self.config = json.load(open("config.json"))
		self.target_ratio = target_ratio
		self.sentences_tokenized = OrderedDict()
		self.meaningful_sentences = list()
		self.garbage_sentences = list()
		self.filtered_text = ""
		return

	def tokenize_part_of_speech(self, text):
		sentences = nltk.sent_tokenize(text)
		for sentence in sentences:
			words = nltk.word_tokenize(sentence)
			self.sentences_tokenized[sentence] = nltk.pos_tag(words)
		return

	def filter_and_purge(self, text):
		# Calculate ratio of filtered parts of speech
		self.tokenize_part_of_speech(text)
		for sentence, pos_tokens in self.sentences_tokenized.items():
			meaningful_word_count = 0
			valid_word_count = 0
			token_count = len(pos_tokens)
			for token in pos_tokens:
				if self.filter_token(token) == True:
					meaningful_word_count += 1
				if not self.filter_token(token) == "neutral":
					valid_word_count += 1
			if valid_word_count > 0 and meaningful_word_count / valid_word_count > self.target_ratio:
				self.meaningful_sentences.append(sentence)
			else:
				self.garbage_sentences.append(sentence)
				# print(sentence)
				# print(str(meaningful_word_count) + " meaningful words / " + str(valid_word_count) + " valid words. " + str(token_count) + " tokens\n")
		self.filtered_text = " ".join(self.meaningful_sentences)
		print(str(len(self.garbage_sentences)) + " out of " + str(len(self.sentences_tokenized)) + " sentences.")
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
