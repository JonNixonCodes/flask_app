#File: sentification_mod.py

import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB

import textblob
import pickle

from textblob import TextBlob

"""
Hacky solution to running script from different directory
"""
import os
preDir = ''
directories = os.getcwd().split('/')
if directories[-1] == 'flask_app':
    preDir = 'SentweetmentProject/'

# load pickle NB
f = open(preDir + 'modules/jar_of_pickles/MNBclassifier.pickle', 'rb')
MNBclassifier = pickle.load(f)
f.close()

# load word features
f = open(preDir + 'modules/jar_of_pickles/stanford_features6000.pickle', 'rb')
word_features = pickle.load(f)
f.close()

# function to find features from text
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
def find_features(text):
    words = tokenizer.tokenize(text)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


class Sentifier:
    classifier_dict = {'TextBlob' : 0, 'NB' : 1}    
    def __init__(self, classifier):
        # load all classifiers
        try:
            self.classifier = self.classifier_dict[classifier]
        except KeyError:
            print('invalid classifier')
        
    def sentiment(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0: return 'pos'
            elif polarity < 0: return 'neg'
            elif polarity == 0: return 'neutral'
            else:
                print('Error: invalid polarity')
    
        elif self.classifier == self.classifier_dict['NB']:
            features = find_features(text)
            return MNBclassifier.classify(features)
    def confidence(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity < 0:
                polarity = -polarity
            return polarity
        elif self.classifier == self.classifier_dict['NB']:
            features = find_features(text)
            probDist = MNBclassifier.prob_classify(features)
            return probDist.prob(probDist.max())
            
        elif self.classifier == self.classifier_dict['NB']:
            features = find_features(text)
            return MNBclassifier.classify(features)
        

    def subjectivity(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            return blob.sentiment.subjectivity
