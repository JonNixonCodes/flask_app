# train NB classifier on tweets from Stanford corpus

import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer
from nltk.corpus import stopwords
import random
import pickle
import re
import string

from nltk.classify.scikitlearn import SklearnClassifier 
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

f = open('modules/jar_of_pickles/stanford_featuresets1600000.pickle', 'rb')
featuresets = pickle.load(f)
f.close()

N = 16000 #number of featuresets
# randomise order of feature set
random.shuffle(featuresets)

training_set = featuresets[:int(N*0.8)]
testing_set = featuresets[int(N*0.8):]
print(len(training_set))
print(len(testing_set))

MNBclassifier = SklearnClassifier(MultinomialNB())
MNBclassifier.train(training_set)
print("MultinomialNB accuracy percent:", nltk.classify.accuracy(MNBclassifier, testing_set))

#pickle classifier
f = open('modules/jar_of_pickles/MNBclassifier.pickle', 'wb')
pickle.dump(MNBclassifier, f)
f.close()

"""
all_words = []
for t in all_tweets:
    tokenizer = RegexpTokenizer(r"\w+'?\w+")
    words = tokenizer.tokenize(t[0])
    for w in words:
        all_words.append(w.lower())

fdist = nltk.FreqDist(all_words)
#print 100 most common words
word_features = list(fdist.most_common())[:100] 
print(word_features)
"""
