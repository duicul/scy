import numpy as np
import matplotlib.pyplot as plt
import json
import traceback


if __name__ == "__main__":
    #f = open("result_backtracking.txt", "r")
    #backtracking = json.loads(f.read())
    back_result_x=[8,10]
    back_result_y=[162629700,16159715000]

    f = open("result_neighborhood.txt", "r")
    neighborhood = json.loads(f.read())
    neighborhood_x=[]
    neighborhood_y=[]
    neighborhood_time={"8":[],"10":[],"50":[],"100":[]}
    for res in neighborhood:
        try:
             neighborhood_x.append(res["size"])
             neighborhood_y.append(res["time"])
             neighborhood_time[str(res["size"])+""].append({"time":res["time"]})
        except:
            print(traceback.format_exc())
            pass
    
    f = open("result_annealing.txt", "r")
    annealing = json.loads(f.read())
    annealing_result_x=[]
    annealing_result_y=[]
    init_temp=[]
    for res in annealing:
        try:
            tmp=res["init_temp"]
            if not tmp in init_temp:
                init_temp.append(tmp)
        except:
            print(traceback.format_exc())
            pass
    print(init_temp)
    annealing_x={}
    annealing_y={}
    annealing_time={"8":[],"10":[],"50":[],"100":[]}
    for i in init_temp:
        annealing_x[i]=[]
        annealing_y[i]=[]
    for res in annealing:
        try:
            tmp=res["init_temp"]
            annealing_x[tmp].append(res["len"])
            annealing_y[tmp].append(res["time"])
            annealing_time[str(res["len"])+""].append({"inittemp":res["init_temp"],"time":res["time"]})
        except:
            print(traceback.format_exc())
            pass
    tenures={"8":[],"10":[],"50":[],"100":[]}
    f = open("result_tabu.txt", "r")
    tabu = json.loads(f.read())
    for i in [8,10,50,100]:
        for res in tabu:
            if res["size"]==i:
                tenures[str(i)+""].append({"tenure":res["tenure"],"time":res["time"]})
    print(tenures)
    print(annealing_time)
    print(neighborhood_time)
    print(annealing_x)
    print(annealing_y)
    plt.xlabel("datasize")
    plt.ylabel("nanoseconds")
    plt.title("Heuristic results")
    plt.plot(np.array(back_result_x),np.array(back_result_y),label="Backtracking")
    for i in init_temp:
        plt.plot(np.array(annealing_x[i]),np.array(annealing_y[i]),label="Annealing"+str(i))
    plt.plot(np.array(neighborhood_x),np.array(neighborhood_y),label="Neighbborhood")
    plt.legend()
    plt.savefig("result.png")
    plt.close()

    file = open("result_plot.txt", "w")
    reta=[]
    ret=[]
    ret.append([{"anneal10/8":annealing_time["10"][i]["time"]/annealing_time["8"][i]["time"] if annealing_time["8"][i]["time"]!=0 else -1}  for i in range(3)])
    ret.append([{"back8/anneal8":back_result_y[0]/annealing_time["8"][i]["time"] if annealing_time["8"][i]["time"]!=0 else -1} for i in range(3)])
    ret.append([{"back10/anneal10":back_result_y[1]/annealing_time["10"][i]["time"] if annealing_time["10"][i]["time"]!=0 else -1} for i in range(3)])
    ret.append([{"tabu10/8":tenures["10"][i]["time"]/tenures["8"][i]["time"] if tenures["8"][i]["time"]!=0 else -1} for i in range(3)])
    ret.append([{"back8/tabu8":back_result_y[0]/tenures["8"][i]["time"] if tenures["8"][i]["time"]!=0 else -1} for i in range(3)])
    ret.append([{"back10/tabu10":back_result_y[1]/tenures["10"][i]["time"] if tenures["10"][i]["time"]!=0 else -1} for i in range(3)])
    print(reta)
    reta.append(ret)
    req=[]
    req.append([{"anneal50/neigh50":annealing_time["50"][i]["time"]/neighborhood_time["50"][0]["time"]}  for i in range(3)])
    req.append([{"anneal100/neigh100":annealing_time["100"][i]["time"]/neighborhood_time["100"][0]["time"]}  for i in range(3)])
    req.append([{"tabu50/neigh50":tenures["50"][i]["time"]/neighborhood_time["50"][0]["time"]}  for i in range(3)])
    req.append([{"tabu100/neigh100":tenures["100"][i]["time"]/neighborhood_time["100"][0]["time"]}  for i in range(3)])
    reta.append(req)
    json.dump(reta,file)
    file.close()
