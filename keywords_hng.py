from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def page_keyword(url):
  article = Article(url)
  article.download()
  content = article.html
  article.parse()
  article.nlp()
  keywords = article.keywords
  return keywords


def BoG_keyword(url):
  sentence = input() #input sentence to run through our bag of words model
  tokenizer = tbt().tokenize
  vectorizer = CountVectorizer(tokenizer = tokenizer,stop_words='english')
  train_features = vectorizer.fit_transform(page_keyword(url))
  result = vectorizer.transform([sentence]).toarray()
  return result

#page_keyword('http://www.insightsbot.com/blog/R8fu5/bag-of-words-algorithm-in-python-introduction') #to check keywords
#BoG_keyword('http://www.insightsbot.com/blog/R8fu5/bag-of-words-algorithm-in-python-introduction') #to run bag of words model
'''input sentence you want to run bag of words model on. 
sentence could be *machine learning and python algorithms are cool* '''