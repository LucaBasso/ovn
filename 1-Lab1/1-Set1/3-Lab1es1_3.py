a=input("Insert a list of numbers: ")
numbers=a.split()
numberList=[int(x) for x in numbers]
boolVar=(numberList[0]==numberList[-1])
print(boolVar)
