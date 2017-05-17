# train NB classifier on tweets from Stanford corpus

import nltk
import random
import pickle

from nltk.classify.scikitlearn import SklearnClassifier 
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

f = open('modules/jar_of_pickles/stanford_featuresets1600000.pickle', 'rb')
featuresets = pickle.load(f)
f.close()

f = open('modules/jar_of_pickles/MNBclassifier.pickle', 'rb')
MNBclassifier = pickle.load(f)
f.close

N = 16000 #number of featuresets
# randomise order of feature set
random.shuffle(featuresets)

testing_set = featuresets[int(N*0.8):]
print(len(testing_set))

print("MultinomialNB accuracy percent:", nltk.classify.accuracy(MNBclassifier, testing_set))
