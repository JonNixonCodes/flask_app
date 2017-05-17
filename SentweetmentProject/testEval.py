import sys
sys.path.append('modules')
import evaluation_mod as E
import sentification_mod as S

sent = S.Sentifier('NB')

eval = E.Evaluator('short_reviews')
accuracy = eval.accuracy(sent, 100)
print('accuracy: ' + str(accuracy))
