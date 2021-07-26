a=[x for x in range(11)]
print(a)
print(a[0])
i=int(input('Inserire un numero: '))
#b=a[i:0]
tot=0
for num in a[i:]:
	tot+=num
print(tot)
