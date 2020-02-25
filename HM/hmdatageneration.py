import json
import random
import time
f = open("data.json", "w")
data={}
sizes=[8,10,50,100]
delta=100
key=""
for size in sizes:
    print(size)
    t=[]
    for i in range(size):
        t.append(random.randint(-delta,delta))
    key="IA"+str(size)
    data[key]=t
f.write(json.dumps(data))
f.close()
print(data["IA8"])
print(data["IA10"])
def backtrack(data,mindev,subset):
    auxsubset=subset
    auxmindev=mindev
    for i in data:
        #print("for"+str(i))
        if i not in subset:
            #print("subset"+str(i))
            aux=backtrack(data,i if mindev==None else mindev+i,subset+[i])
            if auxmindev==None or abs(sum(aux))<auxmindev:
                #print(str(i)+"if"+str(abs(sum(aux))))
                auxsubset=aux
                auxmindev=abs(sum(aux))
    return auxsubset
init=time.time_ns()
sol=backtrack(data["IA8"],None,[])
print(sol)            
print(abs(sum(sol)))
time8=time.time_ns()-init
init=time.time_ns()
sol=backtrack(data["IA10"],None,[])
print(sol)            
print(abs(sum(sol))) 
time10=time.time_ns()-init
print("time8 = "+str(time8))
print("time10 = "+str(time10))
print("divide = "+str(time10/time8))
