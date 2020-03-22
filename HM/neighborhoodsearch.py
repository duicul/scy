import json
import random
import time

def loaddata(filename):
    f = open(filename, "r")
    data=json.loads(f.read())
    f.close()
    return data

def add_el(curr_sol,sol_space):
    neig=[]
    for val in sol_space:
        if val not in curr_sol:
           neig.append(curr_sol+[val])
    return neig

def rem_el(curr_sol,sol_space):
    neig=[]
    print(sol_space)
    for val in sol_space:
        #print(val)
        if val in curr_sol:
            aux=[]+curr_sol
            aux.remove(val)
            neig.append(aux)
    return neig

def localsearch(data,max_same):
    curr_list=data+[]
    curr_val=sum(data)
    same=0
    while same<max_same:
        print("curr val "+str(sum(curr_list)))
        print("curr list "+str(curr_list))
        better=False
        rem_list=rem_el(curr_list,data)
        add_list=add_el(curr_list,data)
        neig=rem_list+add_list
        for n in neig:
            if abs(sum(n))<abs(curr_val):
                curr_list=n
                curr_val=sum(n)
                same=0
                better=True
                break
            if abs(sum(n))==abs(curr_val):
                curr_list=n
                curr_val=sum(n)
                break
        if not better:
            same=same+1


if __name__=='__main__':
    data=loaddata("data.json")
    localsearch(data['IA50'],5)
