name=input("Nume ")
s=0
for i in name:
    s=s if i==' ' else s+ord(i.lower())-ord('a'.lower())+1
    print(i.lower(),s)
while s>9:
    aux=str(s)
    print(aux,"aux")
    s=0
    for i in aux:
        s=s+int(i)
        print(s,"s")

print("Final",s)
