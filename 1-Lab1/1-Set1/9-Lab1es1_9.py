s="ABCdef123,,$$GhiJ32K"
low=0
upp=0
dig=0
spe=0
for car in s:
	if car.isupper():
		upp+=1
	elif car.islower():
		low+=1
	elif car.isdigit():
		dig+=1
	else:
		spe+=1
print("""String: {}
low: {}
upp: {}
dig: {}
spe: {}""".format(s,low,upp,dig,spe))
