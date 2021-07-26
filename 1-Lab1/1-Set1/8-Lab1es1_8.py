import math
s1="0123456789"
s2="abcdefghij"
print(s1[0]+s1[math.ceil(len(s1)/2)]+s1[-1]+s2[0]+s2[math.ceil(len(s2)/2)]+s2[-1])
