import sys
sys.path.append('modules')
import intensification_mod as I

i1 = I.Intensifier('rule')
text = 'WTFFF THAT movie was EPIC!'
upper_case = [c for c in text if c.isupper()]
all_case = [c for c in text if c.isupper() or c.islower()]
capitalisation = len(upper_case)/len(all_case)
print(len(upper_case), len(all_case))
print(i1.intensity(text))
