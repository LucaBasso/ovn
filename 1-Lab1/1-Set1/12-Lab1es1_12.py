s="qwertyuiopasdfghjklzxcvbnm2849347659864MNBVCXZLKJHGFDSA1234567890POIUYrewq1234qwe"
alf="abcdefghijklmnopqrstuvwxyz"
dict={}
count=0
print(s)
for ch in alf:
	dict.update({ch:count})
for caratt in s.lower():
	if caratt.isalpha():
		dict[caratt]+=1
for (i,el) in dict.items():
	print("""key: {} val: {}""".format(i,el))
