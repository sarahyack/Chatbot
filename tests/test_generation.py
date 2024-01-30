# tests/test_generation.py

import unittest
from unittest.mock import MagicMock, patch, mock_open, MagicMock
from unittest import TestCase

from data.data_augmentation.data_generation import *

class TestDataGeneration(TestCase):

    @patch('data.data_augmentation.data_generation.nltk.download')
    def test_summarize(self, mock_nltk_download):
        text = "This is a test sentence. Another sentence for testing. Testing is important. This is extra."
        summary_length = 2

        summary = summarize(text, summary_length)
        summary_sentences = summary.split('.')
        summary_sentences = [sentence.strip() for sentence in summary_sentences if sentence.strip()]

        self.assertLessEqual(len(summary_sentences), summary_length)

        for sentence in summary_sentences:
            self.assertIn(sentence, text)
    
    @patch('data.data_augmentation.data_generation.spacy.load')
    def test_extract_entities(self, mock_spacy_load):
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_entity = MagicMock()
        mock_entity.text = "Python"
        mock_entity.label_ = "ORG"
        mock_doc.ents = [mock_entity]
        mock_nlp.return_value = mock_doc
        mock_spacy_load.return_value = mock_nlp

        text = "Python is a programming language."
        entities = extract_entities(text)

        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0], ("Python", "ORG"))
