import math
s1="0123456789"
s2="ciao"
s3=s1[0:math.ceil((len(s1)/2))]
s4=s1[math.ceil(len(s1)/2):]
print(s3+s2+s4)
