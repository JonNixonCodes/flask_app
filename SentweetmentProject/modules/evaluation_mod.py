#file: evaluation_mod.py
import nltk
from nltk.corpus import movie_reviews
import random
import sentification_mod as sentification

class Evaluator:
    _corpora_dict = {'short_reviews': 0}
    def __init__(self, corpora):
        try:
            self._corpora = self._corpora_dict[corpora]
        except KeyError:
            print('invalid corpora')

    def accuracy(self, sentifier, size_of_testset):
        s = sentifier
        if (self._corpora == self._corpora_dict['short_reviews']):
            pos_rev = open("corpora/short_reviews/positive.txt", encoding="latin-1").read()
            neg_rev = open("corpora/short_reviews/negative.txt", encoding="latin-1").read()
            
            documents = []

            for r in pos_rev.split('\n'):
                documents.append( (r, 'pos') )

            for r in neg_rev.split('\n'):
                documents.append( (r, 'neg') )        

            random.shuffle(documents)

            testing_set = documents[:size_of_testset]
            TP = 0
            FP = 0
            TN = 0
            FN = 0
            for t in testing_set:
                sentiment = s.sentiment(t[0])
                if sentiment > 0:
                    if t[1] == 'pos':
                        TP += 1
                    elif t[1] == 'neg':
                        FP += 1
                elif sentiment < 0:
                    if t[1] == 'neg':
                        TN += 1
                    elif t[1] == 'pos':
                        FN += 1                        
            return (TP + TN)/(TP + FP + TN + FN) * 100
