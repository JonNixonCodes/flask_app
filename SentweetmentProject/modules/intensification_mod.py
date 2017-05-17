#File: subjectification_mod.py
import nltk

import textblob
from textblob import TextBlob

class Intensifier:
    classifier_dict = {'rule' : 0}    
    def __init__(self, classifier):
        # load all classifiers
        try:
            self.classifier = self.classifier_dict[classifier]
        except KeyError:
            print('invalid classifier')
        
    def intensity(self, text):
        if self.classifier == self.classifier_dict['rule']:
            repetition = 0
            upper_case = [c for c in text if c.isupper()]
            all_case = [c for c in text if c.isupper() or c.islower()]
            capitalisation = len(upper_case)/len(all_case)
            for c in range(0, len(text)-2):
                if (text[c] in all_case):
                    if (text[c] == text[c+1] and text[c+1] == text[c+2]):
                        repetition += 1
            retVal = 0
            if capitalisation > 0.25:
                retVal += 0.5
            if capitalisation > 0.5:
                retVal += 0.25
            if repetition >= 1:
                retVal += 0.25
            return retVal
