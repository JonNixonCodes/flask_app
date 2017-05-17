import sys
sys.path.append('modules')

import sentification_mod as sentification

s1 = sentification.Sentifier('TextBlob')
s2 = sentification.Sentifier('NB')

#print (s1.classifier_dict)
text = "Hello world, I'm so happy to finally be here, Yay!"
text2 = "That's random, I expect this should be neutral"
text3 = "This post sucks, and should definitely be negative"
print(text)
print(s1.sentiment(text))
print(s1.confidence(text))
print(s2.sentiment(text))
print(s2.confidence(text))

print(text2)
print(s1.sentiment(text2))
print(s1.confidence(text2))
print(s2.sentiment(text2))
print(s2.confidence(text2))

print(text3)
print(s1.sentiment(text3))
print(s1.confidence(text3))
print(s2.sentiment(text3))
print(s2.confidence(text3))
