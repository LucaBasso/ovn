x=[1, 2, 3.4, 5, 9, 23, 42]
y=[11, 22, 13.4, 15, 19, 123, 142]
print(x,y)
z=[]
for el in x:
	if el%2!=0 and isinstance(el,int):
		print(el)
print("=====================")
for num in y:
	if num%2==0:
		print(num)

