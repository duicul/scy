import json
import random
import time

def generate(filename):
    f = open(filename, "w")
    data={}
    sizes=[8,10,50,100]
    delta=100
    key=""
    for size in sizes:
        print(size)
        t=[random.randint(-delta,delta) for i in range(size)]
        key="IA"+str(size)
        data[key]=t
    f.write(json.dumps(data))
    f.close()
    print(data["IA8"])
    print(data["IA10"])

def loaddata(filename):
    f = open(filename, "r")
    data=json.loads(f.read())
    f.close()
    return data
    
def backtrack(data,mindev,subset):
    auxsubset=subset
    auxmindev=mindev
    for i in data:
        #print("for"+str(i))
        if i not in subset:
            #print("subset"+str(i))
            aux=backtrack(data,i if mindev==None else mindev+i,subset+[i])
            if auxmindev==None or abs(sum(aux))<auxmindev or (abs(sum(aux))==auxmindev and len(aux)>len(auxsubset)):
                #print(str(i)+"if"+str(abs(sum(aux))))
                auxsubset=aux
                auxmindev=abs(sum(aux))
    return auxsubset
init=time.time_ns()
data=loaddata("data.json")
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
