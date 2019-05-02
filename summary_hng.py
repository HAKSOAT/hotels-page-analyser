from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TreebankWordTokenizer as tbt
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def page_summary(url):
  article = Article(url)
  article.download()
  content = article.html
  article.parse()
  article.nlp()
  summary = [article.summary]
  return summary

def BoG_summary(url):
  sentence = input()
  tokenizer = tbt().tokenize
  vectorizer = CountVectorizer(tokenizer = tokenizer,stop_words=stopWords)
  train_data_features = vectorizer.fit_transform(page_summary(url))
  result = vectorizer.transform(sentence).toarray()
  return result

#BoG_summary('http://www.insightsbot.com/blog/R8fu5/bag-of-words-algorithm-in-python-introduction')