import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import os

def plot_datadb(threads_no,datasize,data,prefix,name):
    if not os.path.exists(name):
        os.makedirs(name)
    if not os.path.exists(name+"/threads"):
        os.makedirs(name+"/threads")
    if not os.path.exists(name+"/datasize"):
        os.makedirs(name+"/datasize")
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
            for tv in data:
                try:
                    if int(tv["datasize"]) == ds and int(tv["threads"])==th:
                        array_ds.append(ds)
                        sel=tv["select"]
                        resp_array_val_sel.append(sel["resp"])
                        exec_array_val_sel.append(sel["exec"])
                        ins=tv["insert"]
                        resp_array_val_ins.append(ins["resp"])
                        exec_array_val_ins.append(ins["exec"])
                except KeyError :
                    print(traceback.format_exc())
                    pass
        if len(resp_array_val_sel) <= 1:
            continue
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
        plt.title(str(th)+" Threads total time for datasize\n(datasize split equally per threads)\n"+name)
        plt.legend()
        plt.savefig(name+"/threads/"+prefix+str(th)+".png")
        plt.close()
    for ds in [1000,3000,5000,10000]:
        array_th=[]
        resp_array_val_sel=[]
        exec_array_val_sel=[]
        resp_array_val_ins=[]
        exec_array_val_ins=[]
        for th in threads_no:
            for tv in data:
                try: 
                    if int(tv["datasize"]) == ds and int(tv["threads"])==th:
                        array_th.append(th)
                        sel=tv["select"]
                        resp_array_val_sel.append(sel["resp"])
                        exec_array_val_sel.append(sel["exec"])
                        ins=tv["insert"]
                        resp_array_val_ins.append(ins["resp"])
                        exec_array_val_ins.append(ins["exec"])
                except KeyError:
                    print(traceback.format_exc())
                    pass
        
        if len(resp_array_val_sel) <= 1:
            continue
        x=np.array(array_th)
        y_sel_resp=np.array(resp_array_val_sel)
        y_sel_exec=np.array(exec_array_val_sel)
        y_ins_resp=np.array(resp_array_val_ins)
        y_ins_exec=np.array(exec_array_val_ins)
        plt.xlabel("threads")
        plt.ylabel("ms")
        plt.plot(x,y_sel_resp,label="select response time")
        #plt.plot(x,y_sel_exec,label="select execution time")
        plt.plot(x,y_ins_resp,label="insert response time")
        #plt.plot(x,y_ins_exec,label="insert execution time")
        plt.title(str(ds)+" Datasize total time for for different thread numbers\n"+name)
        plt.legend()
        plt.savefig(name+"/datasize/"+prefix+"data"+str(ds)+".png")
        plt.close()

def compare(datas,names,datasize,threads,directory):
    if not len(datas) == len(names):
        return
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory+"/both"):
        os.makedirs(directory+"/both")
    if not os.path.exists(directory+"/insert"):
        os.makedirs(directory+"/insert")
    if not os.path.exists(directory+"/select"):
        os.makedirs(directory+"/select")
    for th in threads:
        y=[]
        x=np.array(datasize)
        xaux=[]
        for data in datas:
            yaux=[]
            yaux.append([])
            yaux.append([])
            yaux.append([])
            #print(yaux)
            for tv in data:
                xaux=[]
                for ds in datasize:
                     try: 
                        if int(tv["datasize"]) == ds and int(tv["threads"])== th:
                            sel=tv["select"]
                            ins=tv["insert"]
                            yaux[0].append(sel["resp"])
                            yaux[1].append(ins["resp"])
                            yaux[2].append(ds)
                     except KeyError:
                            print(traceback.format_exc())
                            pass
            y.append(yaux)

        x=np.array(xaux)
        plt.xlabel("datasize")
        plt.ylabel("ms")
        comp=""
        suffile=""
        for name in names:
            comp+=name+" "
            suffile+=name
        plt.title("Comparasion between "+str(comp)+"\n"+str(th)+" threads")
        for i in range(len(y)):
            yi=y[i]
            #print(x)
            #print(names)
            name=names[i]
            plt.plot(np.array(yi[2]),np.array(yi[0]),label="select time "+name)
            #plt.plot(x,np.array(yi[1]),label="insert time "+str(names[i]))

        plt.legend()
        plt.savefig(directory+"/select/"+"comparasionselect"+suffile+str(th)+".png")
        plt.close()

        plt.xlabel("datasize")
        plt.ylabel("ms")
        plt.title("Comparasion between "+str(comp)+"\n"+str(th)+" threads")
        for i in range(len(y)):
            yi=y[i]
            #print(x)
            #print(len(y)) 
            #plt.plot(x,np.array(yi[0]),label="select time "+str(names[i]))
            plt.plot(np.array(yi[2]),np.array(yi[1]),label="insert time "+str(names[i]))
        plt.legend()
        plt.savefig(directory+"/insert/"+"comparasioninsert"+suffile+str(th)+".png")
        plt.close()

        plt.xlabel("datasize")
        plt.ylabel("ms")
        plt.title("Comparasion between "+str(comp)+"\n"+str(th)+" threads")
        for i in range(len(y)):
            yi=y[i]
            #print(x)
            #print(len(y))
            name=names[i]
            plt.plot_date(np.array(yi[2]),np.array(yi[0]),label="select time "+name)
            plt.plot_date(np.array(yi[2]),np.array(yi[1]),label="insert time "+name)
        plt.legend()
        plt.savefig(directory+"/both/"+"comparasion"+suffile+str(th)+".png")
        plt.close()

if __name__=="__main__":
    f = open("result_cratedb.txt", "r")
    data_cratedb = json.loads(f.read())
    f.close()
    f = open("result_mariadb.txt", "r")
    data_mariadb = json.loads(f.read())
    f.close()
    f = open("result_sqlite.txt", "r")
    data_sqllite = json.loads(f.read())
    f.close()

    threads_no=[1,5,10,20,50,100]
    datasize=[10,20,30,50,100,200,300,500,1000,2000,3000,4000,5000,10000]
    
    plot_datadb(threads_no,datasize,data_cratedb,"cratedb","CrateDB")
    plot_datadb(threads_no,datasize,data_mariadb,"mariadb","MariaDB")
    plot_datadb(threads_no,datasize,data_sqllite,"sqlite","SQLite")
    compare([data_cratedb,data_mariadb,data_sqllite],["CrateDB","MariaDB","SQLite"],datasize,[1,100],"comparasion")
    compare([data_cratedb,data_mariadb],["CrateDB","MariaDB"],datasize,[1,100],"comparasion")
