import os
from sklearn import model_selection, svm
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

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

	def train_privacy_pages(self, corpus, labels):
		vectorizer = CountVectorizer()
		SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
		classifier = Pipeline([('vectorizer', vectorizer), ('svm', SVM)])
		classifier.fit(corpus, labels)
		current_directory = os.path.dirname(os.path.abspath(__file__))
		models_directory = os.path.join(current_directory, "models")

		if not os.path.exists(models_directory):
			os.makedirs(models_directory)

		file_path = os.path.join(models_directory, "privacy_pages_model.pkl")
		joblib.dump(classifier, file_path)

	def predict_privacy_pages(self, corpus):
		current_directory = os.path.dirname(os.path.abspath(__file__))
		models_directory = os.path.join(current_directory, "models")
		file_path = os.path.join(models_directory, "privacy_pages_model.pkl")
		classifier = joblib.load(file_path)
		predictions = classifier.predict(corpus)
		return predictions

