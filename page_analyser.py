import requests

class PageAnalyser():
	def __init__(self, url):
		self.url = url
		self.page_content = None

	def download_page(self):
		page_object = requests.get(self.url)
		self.page_content = page_object.content