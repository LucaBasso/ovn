l=[11,45,8,11,23,45,23,45,89]
dict={}
for el in l:
	if el in dict:
		dict[el]+=1
	else:
		dict.update({el:1})

for (key,el) in dict.items():
	print("key: {} count: {}".format(key,el))
