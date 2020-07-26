import time,json
import random
from basicfunctions import loaddata, add_el, rem_el, rem_2el
import matplotlib.pyplot as plt
import numpy as np

def equal_sol(sol1, sol2):
    if len(sol1) != len(sol2):
        return False
    for i in sol1:
        if i not in sol2:
            return False
    return True


def determine_x_next(candidate_now):
    # print(len(candidate_now))
    best = candidate_now[0]
    for candi in candidate_now:
        if abs(sum(candi)) < abs(sum(best)) or (abs(sum(candi)) == abs(sum(best)) and len(candi) >= len(best)):
            best = candi
            # print(best)
            # print(abs(sum(best)))

    # print()
    return best


def candidate_now_neigh(hist, current_sol, data_set):
    rem_list = rem_el(current_sol, data_set)
    rem_2list = rem_2el(current_sol, data_set)
    add_list = add_el(current_sol, data_set)
    neig = rem_list + add_list + rem_2list
    candidate_now = []
    for neigi in neig:
        match = False
        for histi in hist:
            if equal_sol(histi[1], neigi):
                match = True
                break
        if not match:
            candidate_now.append(neigi)
    return candidate_now


def remove_short_hist(hist):
    toremove = []
    for i in range(len(hist)):
        hist[i][0] -= 1
        if hist[i][0] == 0:
            toremove += [i]
    for i in toremove:
        del (hist[i])


def det_x_next(hist, current_sol, data_set):
    remove_short_hist(hist)
    # print(len(hist))
    # print(current_sol)
    # print(len(current_sol))
    candidate_now = candidate_now_neigh(hist, current_sol, data_set)
    if(len(candidate_now)==0):
        return current_sol
    x_next = determine_x_next(candidate_now)

    return x_next


def better_sol(current_sol, next_sol):
    """

    :param current_sol: list
    :type next_sol: list
    """
    return abs(sum(current_sol)) < abs(sum(next_sol)) or (
            abs(sum(current_sol)) == abs(sum(next_sol)) and len(current_sol) <= len(next_sol))


def prev_sol_found(prev_sols, next_sol):
    for soli in prev_sols:
        if equal_sol(soli, next_sol):
            return True
    prev_sols.append(next_sol)
    return False


def tabu_search(data_set,short_tabu_steps):
    best_sol = data_set
    hist = []
    count = 0
    hist.append([short_tabu_steps, best_sol])
    same = 0
    next_sol = det_x_next(hist, best_sol, data_set)
    prev_sol = best_sol
    prev_sols = [best_sol]
    intermediate_sol = [best_sol]
    while same < short_tabu_steps+1:

        if better_sol(best_sol, next_sol):
            best_sol = next_sol

        else:
            if len(intermediate_sol)>0:
                best_sol = intermediate_sol.pop()
            intermediate_sol.insert(0, data_set)

        if prev_sol_found(prev_sols,best_sol):
            same += 1
            if len(intermediate_sol)>0:
                best_sol = intermediate_sol.pop()
        # print()
        # print("same" + str(same))
        # print(next_sol)
        # print(best_sol)
        # print()
        """
        if equal_sol(next_sol, best_sol) or equal_sol(next_sol, prev_sol):
            same += 1
        else:
            same = 0"""
        hist.append([short_tabu_steps, next_sol])
        count += 1
        prev_sol = next_sol
        next_sol = det_x_next(hist, best_sol, data_set)
    return best_sol


if __name__ == "__main__":
    data = loaddata("data.json")

    ret=[]
    tenance8=[1,2,3]
    tenance8_y=[[],[]]
    for tenance in tenance8:
        for i in range(10):
            start8=list(set(random.choices(data['IA8'],k=random.randint(3,6))))
            init = time.time_ns()
            l8aux = tabu_search(start8,tenance)
            time8aux = time.time_ns() - init
            #print(l8aux)
            #print(sum(l8aux))
            #print("time8 " + str(time8aux) + " = " + str(time8aux / 1000000000) + "s")
            if i==0 :
                l8=l8aux
                time8=time8aux
            elif abs(sum(l8aux))<abs(sum(l8)):
                l8=l8aux
                time8=time8aux
        tenance8_y[0].append(abs(sum(l8)))
        tenance8_y[1].append(time8)
        ret.append({"size": 8,"tenure":tenance, "time": time8, "times": time8 / 1000000000, "val": sum(l8), "length": len(l8), "list": l8})
    print(tenance8_y)
    
    tenance10=[2,3,4]
    tenance10_y=[[],[]]
    for tenance in tenance10:
        for i in range(10):
            start10=list(set(random.choices(data['IA10'],k=random.randint(3,8))))
            init = time.time_ns()
            l10aux = tabu_search(start10,tenance)
            time10aux = time.time_ns() - init
            #print(l10aux)
            #print(sum(l10aux))
            #print("time10 " + str(time10aux) + " = " + str(time10aux / 1000000000) + "s")
            if i==0 :
                l10=l10aux
                time10=time10aux
            elif abs(sum(l10aux))<abs(sum(l10)):
                l10=l10aux
                time10=time10aux
        tenance10_y[0].append(abs(sum(l10)))
        tenance10_y[1].append(time10)
        ret.append({"size": 10,"tenure":tenance, "time": time10, "times": time10 / 1000000000, "val": sum(l10), "length": len(l10), "list": l10})
    print(tenance10_y)
    
    tenance50=[20,30,40]
    tenance50_y=[[],[]]
    for tenance in tenance50:
        for i in range(10):
            start50=list(set(random.choices(data['IA50'],k=random.randint(3,45))))
            init = time.time_ns()
            l50aux = tabu_search(start50,tenance)
            time50aux = time.time_ns() - init
            #print(l50aux)
            #print(sum(l50aux))
            #print("time50 " + str(time50aux) + " = " + str(time50aux / 1000000000) + "s")
            if i==0 :
                l50=l50aux
                time50=time50aux
            elif abs(sum(l50aux))<abs(sum(l50)):
                l50=l50aux
                time50=time50aux
        tenance50_y[0].append(abs(sum(l50)))
        tenance50_y[1].append(time50)
        ret.append({"size": 50,"tenure":tenance, "time": time50, "times": time50 / 1000000000, "val": sum(l50), "length": len(l50), "list": l50})
    print(tenance50_y)
    
    tenance100=[30,40,50]
    tenance100_y=[[],[]]
    for tenance in tenance100:
        for i in range(10):
            start100=list(set(random.choices(data['IA100'],k=random.randint(3,95))))
            init = time.time_ns()
            l100aux = tabu_search(start100,tenance)
            time100aux = time.time_ns() - init
            #print(l100aux)
            #print(sum(l100aux))
            #print("time100 " + str(time100aux) + " = " + str(time100aux / 1000000000) + "s")
            if i==0 :
                l100=l100aux
                time100=time100aux
            elif abs(sum(l100aux))<abs(sum(l100)):
                l100=l100aux
                time100=time100aux
        tenance100_y[0].append(abs(sum(l100)))
        tenance100_y[1].append(time100)
        ret.append({"size": 100,"tenure":tenance, "time": time100, "times": time100 / 1000000000, "val": sum(l100), "length": len(l100),"list": l100})
    print(tenance100_y)
    
    plt.xlabel("tenure")
    plt.ylabel("error")
    plt.title("Tabu search tenure variation")
    plt.plot(np.array(tenance8),np.array(tenance8_y[0]),label="Value8")
    plt.plot(np.array(tenance10),np.array(tenance10_y[0]),label="Value10")
    plt.plot(np.array(tenance50),np.array(tenance50_y[0]),label="Value50")
    plt.plot(np.array(tenance100),np.array(tenance100_y[0]),label="Value100")
    plt.legend()
    plt.savefig("tenure_value.png")
    plt.close()

    plt.xlabel("tenure")
    plt.ylabel("nanoseconds")
    plt.title("Tabu search tenure variation")
    plt.plot(np.array(tenance8),np.array(tenance8_y[1]),label="Time8")
    plt.plot(np.array(tenance10),np.array(tenance10_y[1]),label="Time10")
    plt.plot(np.array(tenance50),np.array(tenance50_y[1]),label="Time50")
    plt.plot(np.array(tenance100),np.array(tenance100_y[1]),label="Time100")
    plt.legend()
    plt.savefig("tenure_time.png")
    plt.close()
    
    file = open("result_tabu.txt", "w")
    json.dump(ret,file)
    #file.write(str(ret))
    file.close()
    print("finish")
