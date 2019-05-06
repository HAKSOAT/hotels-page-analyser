class PageClassifier():
	def __init__(self, data_structure):
		self.data_structure = data_structure

	def get_corpus_labels_urls(self, keyword):
		labels = []
		urls = []
		corpus = []
		for mapping in self.data_structure:
			for key, site in mapping.items():
				for key, page in site.items():
				page = page[0]
				corpus.append("{} {} {}".format(page["short_url"], page["keywords"],
												page["anchor_tags"], page["h1"]))
				if keyword in page["short_url"]:
				       labels.append(1)
				else:
				       labels.append(0)
				urls.append(page["url"])

		return (corpus, labels, urls)

