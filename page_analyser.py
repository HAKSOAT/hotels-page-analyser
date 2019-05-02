import argparse
from bs4 import BeautifulSoup as bs
from newspaper import Article
import numpy
import re
import requests


class PageAnalyser():
	def __init__(self, url):
		self.url = url
		self.page_content = None
		self.parsed_page_content = None
		self.anchor_tags = None
		self.href_values = []
		self.anchor_texts = []
		self.h_tags = None
		self.h_tag_texts = []
		self.bag_of_words = []

	def download_page(self):
		try:
			# Some sites do not allow requests without headers
			# The headers dictionary deals with this
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
			AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
			# requests.get only works with urls with http or https
			if re.match(r"(https://|http://).+", self.url):
				page_object = requests.get(self.url, headers=headers)
			else:
				page_object = requests.get("https://{}".format(self.url), headers=headers)
			self.page_content = page_object.content
		except requests.exceptions.ConnectionError:
			print("Error: Something is wrong with the url")

	def parse_page(self):
		if self.page_content is None:
			print("Error: Page content has not been loaded")
		else:
			self.parsed_page_content = bs(self.page_content, "html.parser")

	def find_anchor_tags(self):
		if self.parsed_page_content is None:
			print("Error: Page content has not been parsed")
		else:
			self.anchor_tags = self.parsed_page_content.find_all("a")

	def find_href_values(self):
		if self.anchor_tags is None:
			print("Error: There are no anchor tags")
		else:
			for anchor_tag in self.anchor_tags:
				# Some anchor tags do not have href attributes
				# Use an empty string as the href value of such tags
				try:
					self.href_values.append(anchor_tag["href"])
				except KeyError:
					self.href_values.append("")

	def find_anchor_texts(self):
		if self.anchor_tags is None:
			print("Error: There are no anchor tags")
		else:
			for anchor_tag in self.anchor_tags:
				self.anchor_texts.append(anchor_tag.text.strip())

	def get_links_and_texts(self):
		links_and_texts = list(zip(self.href_values, self.anchor_texts))
		return links_and_texts

	def find_h_tags(self):
		if self.parsed_page_content is None:
			print("Error: Page content has not been parsed")
		else:
			self.h_tags = self.parsed_page_content.find_all("h1")
			self.h_tags += self.parsed_page_content.find_all("h2")
			self.h_tags += self.parsed_page_content.find_all("h3")

	def find_h_tag_texts(self):
		if self.h_tags is None:
			print("Error: There are no h tags")
		else:
			for h_tag in self.h_tags:
				self.h_tag_texts.append(h_tag.text.strip())

	def clean_text(self, text):
		ignored_words = ['a', "the", "is"]
		words = re.sub("[^\w]", " ",  text).split()
		cleaned_text = [word.lower() for word in words if word not in ignored_words]
		return cleaned_text

	def tokenize(self, texts):
		words = []
		for text in texts:
		    cleaned_text = self.clean_text(text)
		    words.extend(cleaned_text)   
		words = sorted(list(set(words)))
		return words

	def get_bag_of_words(self):
		texts = self.h_tag_texts
		vocab = self.tokenize(self.h_tag_texts)
		for text in texts:
			cleaned_texts = self.clean_text(text)
			bag_vector = numpy.zeros(len(vocab))
			for cleaned_text in cleaned_texts:
				for index, word in enumerate(vocab):
					if word == cleaned_text: 
						bag_vector[index] += 1
			self.bag_of_words.append((text, numpy.array(bag_vector)))
		return self.bag_of_words
  
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--link", help='add a url to test', type=str)
	args = parser.parse_args()
	pageanalyser = PageAnalyser(args.link)
	pageanalyser.download_page()
	pageanalyser.parse_page()
	pageanalyser.find_anchor_tags()
	pageanalyser.find_href_values()
	pageanalyser.find_anchor_texts()
	pageanalyser.find_h_tags()
	pageanalyser.find_h_tag_texts()
	print(pageanalyser.get_bag_of_words())
	
if __name__ == '__main__':
	main()