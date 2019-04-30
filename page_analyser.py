import requests
from bs4 import BeautifulSoup as bs

class PageAnalyser():
	def __init__(self, url):
		self.url = url
		self.page_content = None
		self.parsed_page_content = None

	def download_page(self):
		page_object = requests.get(self.url)
		self.page_content = page_object.content

	def parse_page(self):
		self.parsed_page_content = bs(self.page_content, "html.parser")

		