import numpy as np
import matplotlib.pyplot as plt
import json

def plot_cratedb(threads_no,datasize):
    resp_array_sel=[]
    resp_array_val_sel=[]
    exec_array_sel=[]
    exec_array_val_sel=[]
    resp_array_ins=[]
    resp_array_val_ins=[]
    exec_array_ins=[]
    exec_array_val_ins=[]
    for th in threads_no:
        array_ds=[]
        resp_array_val_sel=[]
        exec_array_val_sel=[]
        resp_array_val_ins=[]
        exec_array_val_ins=[]
        for ds in datasize:
            for tv in data_cratedb:
                if int(tv["datasize"]) == ds and int(tv["threads"])==th:
                    array_ds.append(ds)
                    sel=tv["select"]
                    resp_array_val_sel.append(sel["resp"])
                    exec_array_val_sel.append(sel["exec"])
                    ins=tv["insert"]
                    resp_array_val_ins.append(ins["resp"])
                    exec_array_val_ins.append(ins["exec"])
        x=np.array(array_ds)
        y_sel_resp=np.array(resp_array_val_sel)
        y_sel_exec=np.array(exec_array_val_sel)
        y_ins_resp=np.array(resp_array_val_ins)
        y_ins_exec=np.array(exec_array_val_ins)
        plt.xlabel("Data size")
        plt.ylabel("ms")
        plt.plot(x,y_sel_resp,label="select response time")
        #plt.plot(x,y_sel_exec,label="select execution time")
        plt.plot(x,y_ins_resp,label="insert response time")
        #plt.plot(x,y_ins_exec,label="insert execution time")
        plt.title(str(th)+" Threads total time for datasize\n(datasize split equally per threads)")
        plt.legend()
        plt.savefig("cratedb"+str(th)+".png")
        plt.close()

f = open("result_cratedb.txt", "r")
data_cratedb = json.loads(f.read())
f.close()

threads_no=[1,5,10,20,50,100]
datasize=[10,20,30,50,100,200,300,500,1000,2000,3000,4000,5000,10000]
plot_cratedb(threads_no,datasize)
