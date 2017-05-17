import sys
sys.path.append('modules')
import subjectification_mod as S

s1 = S.Subjectifier('TextBlob')
text = 'That movie was so great'
print(s1.subjectivity(text))
