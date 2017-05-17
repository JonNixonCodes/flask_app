#File: subjectification_mod.py

import nltk

import textblob
from textblob import TextBlob

class Subjectifier:
    classifier_dict = {'TextBlob' : 0}    
    def __init__(self, classifier):
        # load all classifiers
        try:
            self.classifier = self.classifier_dict[classifier]
        except KeyError:
            print('invalid classifier')
        
    def subjectivity(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            return blob.sentiment.subjectivity
