# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = input("Text to analyze.")
u = text.encode("utf-8")
document = types.Document(
    content=u,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text

def sentiment(document):
    print('Text: {}'.format(u))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    return client.analyze_sentiment(document=document).document_sentiment

def syntax_text(text):

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    for token in tokens:
        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))

import argparse
import io
import json
import os

from google.cloud import language_v1beta2
from google.cloud.language_v1beta2 import enums
from google.cloud.language_v1beta2 import types

import numpy
import six
#
# def classify_text(text, verbose=True):
#     """Classify the input text into categories. """
#
#     language_client = language_v1beta2.LanguageServiceClient()
#
#     document = types.Document(
#         content=text,
#         type=enums.Document.Type.PLAIN_TEXT)
#     response = language_client.classify_text(document)
#     categories = response.categories
#
#     result = {}
#
#     for category in categories:
#         # Turn the categories into a dictionary of the form:
#         # {category.name: category.confidence}, so that they can
#         # be treated as a sparse vector.
#         result[category.name] = category.confidence
#
#     if verbose:
#         print(text)
#         for category in categories:
#             print(u'=' * 20)
#             print(u'{:<16}: {}'.format('category', category.name))
#             print(u'{:<16}: {}'.format('confidence', category.confidence))
# s
#     return result
#
