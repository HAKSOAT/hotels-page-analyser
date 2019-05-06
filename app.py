import argparse
import csv
from page_analyser import PageAnalyser
from page_classifier import PageClassifier

def main():  #this calls the class and the methods. Coded by @Haks
	parser = argparse.ArgumentParser()
	train_help_message = "Use to train models, models current available for training are:\n 'privacy'"
	parser.add_argument("-t", "--train", help=train_help_message, type=str)
	parser.add_argument("-ppp", "--predictprivacy", help="Use to predict privacy pages", type=str)
	args = parser.parse_args()

	if args.train == "privacy":
		current_directory = os.path.dirname(os.path.abspath(__file__))
		dataset_directory = os.path.join(current_directory, "dataset")
		file_path = os.path.join(dataset_directory, "sites.csv")
		with open(file_path) as f:
			rows = csv.reader(f)
			links = [row for row in rows]
		for link in links[:1]:
			pageanalyser = PageAnalyser(link[0])
			page_content = pageanalyser.get_page_content()
			if page_content is None:
				continue
			try:
				links_and_anchor_texts = pageanalyser.get_all_links_and_anchor_texts(page_content)
				internal_links_and_anchor_texts = pageanalyser.get_internal_links_and_anchor_texts(links_and_anchor_texts)
				print("Getting meta data, this may take a while.")
				meta_data = pageanalyser.get_meta_data(internal_links_and_anchor_texts)
				pageanalyser.get_data_structure(meta_data)
			except:
				continue

		data_structure = PageAnalyser.data_structure
		pageclassifier = PageClassifier(data_structure)
		corpus, labels, urls = pageclassifier.get_corpus_labels_urls("privacy")
		pageclassifier.train_privacy_pages(corpus, labels)

	elif args.predictprivacy:
		link = args.predictprivacy
		pageanalyser = PageAnalyser(link)
		page_content = pageanalyser.get_page_content()
		
		if page_content is None:
			quit()
		
		try:
			links_and_anchor_texts = pageanalyser.get_all_links_and_anchor_texts(page_content)
			internal_links_and_anchor_texts = pageanalyser.get_internal_links_and_anchor_texts(links_and_anchor_texts)
			print("Getting metadata, this may take a while.")
			meta_data = pageanalyser.get_meta_data(internal_links_and_anchor_texts)
			pageanalyser.get_data_structure(meta_data)
			data_structure = PageAnalyser.data_structure
			pageclassifier = PageClassifier(data_structure)
			corpus, _, urls = pageclassifier.get_corpus_labels_urls("privacy")
			predictions = pageclassifier.predict_privacy_pages(corpus)
			
			for prediction, url in zip(predictions, urls):
				print(prediction, url)

		except Exception as e:
			print("Sorry something broke")
		
	
if __name__ == '__main__':
	main()