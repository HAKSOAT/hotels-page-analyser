import os
from sklearn import model_selection, svm
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
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

	def save_model(self, classifier, file_name):
		current_directory = os.path.dirname(os.path.abspath(__file__))
		models_directory = os.path.join(current_directory, "models")

		if not os.path.exists(models_directory):
			os.makedirs(models_directory)

		file_path = os.path.join(models_directory, file_name)
		joblib.dump(classifier, file_path)

	def load_model(self, file_name):
		current_directory = os.path.dirname(os.path.abspath(__file__))
		models_directory = os.path.join(current_directory, "models")
		file_path = os.path.join(models_directory, file_name)
		classifier = joblib.load(file_path)
		return classifier

	def train_privacy_pages(self, corpus, labels):
		vectorizer = CountVectorizer()
		SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
		classifier = Pipeline([('vectorizer', vectorizer), ('svm', SVM)])
		classifier.fit(corpus, labels)
		self.save_model(classifier, "privacy_pages_model.pkl")

	def predict_privacy_pages(self, corpus):
		classifier = self.load_model("privacy_pages_model.pkl")
		predictions = classifier.predict(corpus)
		return predictions

	def train_about_pages(self, corpus, labels):
		vectorizer= CountVectorizer()		
		multinomial_nb = MultinomialNB(alpha=0.1)
		classifier = Pipeline([('CountVectorizer', vectorizer), ('naivebayes', multinomial_nb)])
		classifier.fit(corpus, labels)
		self.save_model(classifier, "about_pages_model.pkl")

	def predict_about_pages(self, corpus):
		classifier = self.load_model("about_pages_model.pkl")
		predictions = classifier.predict(corpus)
		return predictions

