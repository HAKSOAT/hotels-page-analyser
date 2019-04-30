import requests
from bs4 import BeautifulSoup as bs

class PageAnalyser():
	def __init__(self, url):
		self.url = url
		self.page_content = None
		self.parsed_page_content = None
		self.anchor_tags = None
		self.href_values = []
		self.anchor_text = []

	def download_page(self):
		try:
			if "https://" not in self.url:
				page_object = requests.get("https://{}".format(self.url))
			else:
				page_object = requests.get(self.url)
		except requests.exceptions.ConnectionError:
			print("Error: Something is wrong with the url")
		self.page_content = page_object.content

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
				self.href_values.append(anchor_tag["href"])

	def find_anchor_texts(self):
		if self.anchor_tags is None:
			print("Error: There are no anchor tags")
		else:
			for anchor_tag in self.anchor_tags:
				self.anchor_text.append(anchor_tag.text.strip())