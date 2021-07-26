s="cnsdiueowsb123lfds3m908,masdé*69"
sum=0
num=0
for caratt in s:
	if caratt.isdigit():
		sum+=int(caratt)
		num+=1
print(s)
print("""sum= {}
num= {}
avg= {}""".format(sum,num,sum/num))
