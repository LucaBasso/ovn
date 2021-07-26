import re

stringIn="Emma is a good developer. Emma is also a writer"
count=0
for string in (re.split(" ",stringIn)):
	print(string)
	if(string=="Emma"):
		count+=1
print(count)
