import argparse
import csv
import os
from page_analyser import PageAnalyser
from page_classifier import PageClassifier

def main():  #this calls the class and the methods. Coded by @Haks
	parser = argparse.ArgumentParser()
	train_help_message = "Use to train models, models current available for training are:\n 'privacy'"
	parser.add_argument("-t", "--train", help=train_help_message, type=str)
	parser.add_argument("-ppp", "--predictprivacy", help="Use to predict privacy pages", type=str)
	args = parser.parse_args()

	# Runs the code here when user wants to train the privacy model
	if args.train == "privacy":
		# Create a directory for the dataset to keep the csv files
		current_directory = os.path.dirname(os.path.abspath(__file__))
		dataset_directory = os.path.join(current_directory, "dataset")
		file_path = os.path.join(dataset_directory, "sites.csv")
		with open(file_path) as f:
			rows = csv.reader(f)
			links = [row for row in rows]
		# Get a data structure from the links stated in the dataset
		for link in links[:20]:
			pageanalyser = PageAnalyser(link[0])
			page_content = pageanalyser.get_page_content()
			# Deals with links that do not return anything
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

		# Extract the data structure, create a corpus and train the model
		data_structure = PageAnalyser.data_structure
		pageclassifier = PageClassifier(data_structure)
		corpus, labels, urls = pageclassifier.get_corpus_labels_urls("privacy")
		pageclassifier.train_privacy_pages(corpus, labels)

	# Runs the code here when user wants to predict privacy pages based on the trained model
	elif args.predictprivacy:
		link = args.predictprivacy
		pageanalyser = PageAnalyser(link)
		page_content = pageanalyser.get_page_content()

		# Script should quit if nothing exists in the url inputted
		if page_content is None:
			quit()
		
		# Extract the data structure and create a corpus
		links_and_anchor_texts = pageanalyser.get_all_links_and_anchor_texts(page_content)
		internal_links_and_anchor_texts = pageanalyser.get_internal_links_and_anchor_texts(links_and_anchor_texts)
		print("Getting metadata, this may take a while.")
		meta_data = pageanalyser.get_meta_data(internal_links_and_anchor_texts)
		pageanalyser.get_data_structure(meta_data)
		data_structure = PageAnalyser.data_structure
		pageclassifier = PageClassifier(data_structure)
		corpus, _, urls = pageclassifier.get_corpus_labels_urls("privacy")

		# JavaScript intensive sites will come up with lots of errors
		# Such as the unavailabilty of links in the returned content from requests
		# This triggers an error when predicting, so try and except deals with that
		try:
			predictions = pageclassifier.predict_privacy_pages(corpus)
			
			if 1 in predictions:
				for prediction, url in zip(predictions, urls):
					if prediction == 1:
						print("{} ===>>> Privacy Page".format(url))
			else:
				print("No Privacy Page")

		except ValueError:
			print("Sadly, the url doesn't like to be scraped")

		
	
if __name__ == '__main__':
	main()