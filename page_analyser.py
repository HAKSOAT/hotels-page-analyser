import argparse
from bs4 import BeautifulSoup as bs
from newspaper import Article
import numpy
import re
import requests
from urllib.parse import urlparse
from urllib.parse import urlsplit


class PageAnalyser():
	def __init__(self, url):
		# requests.get only works with urls with http or https
		# so the url needs to have http or https in it
		if re.match(r"(https://|http://).+", url):
			self.url = url
		else:
			self.url = "http://{}".format(url)

	def get_page_content(self, url=None):
		if url is None:
			url = self.url 
		try:
			# Some sites do not allow requests without headers
			# The headers dictionary deals with this
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
			AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}			
			page_object = requests.get(url, headers=headers)
			page_content = page_object.content
		except requests.exceptions.ConnectionError:
			print("Error: Something is wrong with the url")
		parsed_page_content = bs(page_content, "html.parser")
		return parsed_page_content

	def get_all_links_and_anchor_texts(self, page_content):
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

	def get_link_one_level_down(self, link):
		scheme = urlsplit(link).scheme
		netloc = urlsplit(link).netloc
		if((scheme == '') | (netloc == '')):
			return link
		base_url='://'.join([urlsplit(link).scheme,urlsplit(link).netloc])
		path=urlsplit(link).path
		path=path.split('/')
		one_level = [base_url, path[1]]
		return '/'.join(one_level)

	def get_internal_links_and_anchor_texts(self, links_and_anchor_texts):
		link_text_mapping = {}
		domain_name = urlparse(self.url).netloc
		for link, anchor_text in links_and_anchor_texts:
			link_domain_name = urlparse(link).netloc
			if (link_domain_name == domain_name):
				link_one_level_deep = self.get_link_one_level_down(link)
				print(link_one_level_deep)
				link_text_mapping.setdefault(link_one_level_deep,[]).append(anchor_text)
		return link_text_mapping

	def get_meta_data(self, link_text_mapping):
		for link, anchor_text in link_text_mapping.items():
			# requests.get only works with urls with http or https
			# so the url needs to have http or https in it
			if not re.match(r"(https://|http://).+", link):
				link = "http://{}".format(link)
			article = Article(link)
			article.download()
			content = article.html
			article.parse()
			article.nlp()
			keywords = article.keywords
			summary = article.summary
			data = self.get_page_content(link)
			h1=[i.get_text() for i  in data.find_all("h1")]
			return(link,anchor_text, h1, summary, keywords)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--link", help='add a url to test', type=str)
	args = parser.parse_args()
	pageanalyser = PageAnalyser(args.link)
	page_content = pageanalyser.get_page_content()
	links_and_anchor_texts = pageanalyser.get_all_links_and_anchor_texts(page_content)
	internal_links_and_anchor_texts = pageanalyser.get_internal_links_and_anchor_texts(links_and_anchor_texts)
	meta_data = pageanalyser.get_meta_data(internal_links_and_anchor_texts)
	
if __name__ == '__main__':
	main()