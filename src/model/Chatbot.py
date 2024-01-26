import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Sample text
text = "NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources."

# Tokenization
print("---- Tokenization ----")
words = word_tokenize(text)
sentences = sent_tokenize(text)
print(f"Words: {words}")
print(f"Sentences: {sentences}\n")

# Normalization
# Lowercasing
words = [word.lower() for word in words]

# Removing Stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]

# Stemming
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in filtered_words]

# Lemmatization
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

print("---- Text Normalization ----")
print(f"Filtered Words (Stop words removed): {filtered_words}")
print(f"Stemmed Words: {stemmed_words}")
print(f"Lemmatized Words: {lemmatized_words}\n")

# Bag of Words
print("---- Bag of Words ----")
bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(sentences).toarray()
print(f"Bag of Words Vector: \n{bow}\n")
print(f"Feature Names: {bow_vectorizer.get_feature_names_out()}\n")

# TF-IDF
print("---- TF-IDF ----")
tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(sentences).toarray()
print(f"TF-IDF Vector: \n{tfidf}\n")
print(f"Feature Names: {tfidf_vectorizer.get_feature_names_out()}\n")
