import argparse
from bs4 import BeautifulSoup as bs
from newspaper import Article
import numpy
import re
import requests


class PageAnalyser():
	def __init__(self, url):
		self.url = url

	def get_page_content(self):
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
			page_content = page_object.content
		except requests.exceptions.ConnectionError:
			print("Error: Something is wrong with the url")
		parsed_page_content = bs(page_content, "html.parser")
		return parsed_page_content

	def get_links_and_anchor_texts(self, page_content):
		anchor_tags = page_content.find_all("a")
		links = []
		anchor_text = []
		for anchor_tag in anchor_tags:
			# Some anchor tags do not have href attributes
			# Use an empty string as the href value of such tags
			try:
				links.append(anchor_tag["href"])
			except KeyError:
				links.append("")
			anchor_text.append(anchor_tag.text.strip())
		links_and_anchor_texts = list(zip(links, anchor_text))
		return links_and_anchor_texts

  
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--link", help='add a url to test', type=str)
	args = parser.parse_args()
	pageanalyser = PageAnalyser(args.link)
	page_content = pageanalyser.get_page_content()
	links_and_anchor_texts = pageanalyser.get_links_and_anchor_texts(page_content)
	print(links_and_anchor_texts)

	
if __name__ == '__main__':
	main()