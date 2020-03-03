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
time8=time.time_ns()-init
print(sol)            
print(abs(sum(sol)))
init=time.time_ns()
sol=backtrack(data["IA10"],None,[])
time10=time.time_ns()-init
print(sol)            
print(abs(sum(sol))) 
print("time8 = "+str(time8))
print("time10 = "+str(time10))
print("divide = "+str(time10/time8))
card(op(8))=A(8,1)*...*A(8,8)=(8!*8!*8!*8!*8!*8!*8!*8!)/(7!*6!*5!*4!*3!*2!*1!*0!)
card(op(10))=A(10,1)*...*A(10,10)=(10!*10!*10!*10!*10!*10!*10!*10!*10!*10!)/(9!*8!*7!*6!*5!*4!*3!*2!*1!*0!)
card(op(10))/card(op(8))=(9^8*10^8*10!*10!)/(9!*8!)=9^8*10^8*10*9*10=10^10*9^9
