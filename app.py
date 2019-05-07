import argparse
import csv
import os
from page_analyser import PageAnalyser
from page_classifier import PageClassifier

def main():  #this calls the class and the methods. Coded by @Haks
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--train", help="Use to train models", type=str)
	parser.add_argument("-p", "--predict", help="Use to predict pages", type=str)
	parser.add_argument("-n", "--number", help="Use to choose the number of sites to train with", type=int)
	args = parser.parse_args()

	# Raise an error if user doesn't input number of pages to train with
	if (args.train and not args.number):
		parser.error("To train the model, you need to pass in the number of links to be used")

    # Runs the code here when user wants to train the models
    if args.train:
        # Create a directory for the dataset to keep the csv files
        current_directory = os.path.dirname(os.path.abspath(__file__))
        dataset_directory = os.path.join(current_directory, "dataset")
        file_path = os.path.join(dataset_directory, args.train)
        try:
            with open(file_path) as f:
                rows = csv.reader(f)
                links = [row for row in rows]
        except FileNotFoundError:
            parser.error("File does not exist!!!")
        # Get a data structure from the links stated in the dataset
        number_of_links = args.number
        for link in links[:number_of_links]:
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

		# Extract the data structure, create a corpus and train the models
		data_structure = PageAnalyser.data_structure
		pageclassifier = PageClassifier(data_structure)
		privacy_corpus, privacy_labels, _ = pageclassifier.get_corpus_labels_urls("privacy")
		about_corpus, about_labels, _ = pageclassifier.get_corpus_labels_urls("about")
		gallery_corpus, gallery_labels, _ = pageclassifier.get_corpus_labels_urls("gallery")
		rooms_corpus, rooms_labels, _ = pageclassifier.get_corpus_labels_urls("room")
    contact_corpus, contact_labels, _ = pageclassifier.get_corpus_labels_urls("contact")

		pageclassifier.train_privacy_pages(privacy_corpus, privacy_labels)
		pageclassifier.train_about_pages(about_corpus, about_labels)
		pageclassifier.train_gallery_pages(gallery_corpus, gallery_labels)
		pageclassifier.train_rooms_pages(rooms_corpus,rooms_labels)
    pageclassifier.train_rooms_pages(contact_corpus, contact_labels)

		print("Training Complete")

    # Runs the code here when user wants to predict pages based on the trained models
    elif args.predict:
        link = args.predict
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
        corpus, _, urls = pageclassifier.get_corpus_labels_urls("")

		# JavaScript intensive sites will come up with lots of errors
		# Such as the unavailabilty of links in the returned content from requests
		# This triggers an error when predicting, so try and except deals with that
		try:
			privacy_predictions = pageclassifier.predict_privacy_pages(corpus)
			about_predictions = pageclassifier.predict_about_pages(corpus)
			gallery_predictions = pageclassifier.predict_gallery_pages(corpus)
			rooms_predictions = pageclassifier.predict_rooms_pages(corpus)
      contact_predictions = pageclassifier.predict_contact_pages(corpus)


			if 1 in about_predictions:
				for prediction, url in zip(about_predictions, urls):
					if prediction == 1:
						print("{} ===>>> About Page".format(url))
			else:
				print("No About Page")
			
			if 1 in privacy_predictions:
				for prediction, url in zip(privacy_predictions, urls):
					if prediction == 1:
						print("{} ===>>> Privacy Page".format(url))
			else:
				print("No Privacy Page")
				
			if 1 in gallery_predictions:
				for prediction, url in zip(gallery_predictions, urls):
					if prediction == 1:
						print("{} ===>>> Gallery Page".format(url))
			else:
				print("No Gallery Page")

      if 1 in rooms_predictions:
          for prediction, url in zip(rooms_predictions, urls):
              if prediction == 1:
                  print("{} ===>>> Rooms Page".format(url))
      else:
          print("No Rooms Page")


      if 1 in contact_predictions:
          for prediction, url in zip(contact_predictions, urls):
              if prediction == 1:
                  print("{} ===>>> Contact Page".format(url))
      else:
          print("No Contact Page")

    except ValueError:
        print("Sadly, the url doesn't like to be scraped")

        
    
if __name__ == '__main__':
    main()