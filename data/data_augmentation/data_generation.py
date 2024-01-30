# data/data_augmentation/data_generation.py

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
from heapq import nlargest

def summarize(text: str, summary_length: int) -> str:
    """
    Summarize text using NLTK and return the summary as a string.

    Parameters:
        - text (str): The text to summarize.

    Returns:
        - summary (str): The summary of the text.
    '''
    """
    nltk.download("punkt")
    nltk.download("stopwords")
    
    stop_words = set(stopwords.words("english"))
    word_frequencies = defaultdict(int)
    words = word_tokenize(text)
    
    for word in words:
        word = word.lower()
        if word not in stop_words:
            word_frequencies[word] += 1
    
    sentence_tokens = sent_tokenize(text)
    sentence_scores = defaultdict(int)
    
    for sent in sentence_tokens:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if word in word_frequencies:
                    sentence_scores[sent] += word_frequencies[word]

    summary_sentences = nlargest(summary_length, sentence_scores, key=lambda sent: sentence_scores[sent])
    return ' '.join(summary_sentences)

def extract_entities(text):
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

def main():
    # TODO: Add code here
    
    
    
    pass