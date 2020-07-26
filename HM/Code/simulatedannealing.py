import json
import random
import time
import math

from basicfunctions import loaddata, add_el, rem_el, rem_2el, alfasecond


def simulated_annealing(data, nred, init_temp, templen, coolrate):
    s0 = data
    temp = init_temp
    count = 0
    count_total = 0
    count_random = 0
    while temp > (init_temp - templen):
        # print(str(temp)+" "+str(init_temp-templen))
        count = 0
        while count < nred:
            rem_list = rem_el(s0, data)
            rem_2list = rem_2el(s0, data)
            add_list = add_el(s0, data)
            neig = rem_list + add_list + rem_2list
            rand_ind = random.randint(0, len(neig) - 1)
            s = neig[rand_ind]
            delta = abs(sum(s)) - abs(sum(s0))
            count += 1
            count_total += 1
            # print(len(neig))
            if delta < 0 or (delta == 0 and len(s) > len(s0)):
                s0 = s
            else:
                x = random.random()
                if x < math.exp(-delta / temp):
                    # print(temp)
                    count_random += 1
                    s0 = s
        temp = alfasecond(temp, coolrate)
    # print(str(temp)+" "+str(init_temp-templen))
    print(count_random)
    print(count_total)
    return s0


if __name__ == "__main__":
    data = loaddata("data.json")
    nred = 100
    # beta=0.0001
    inittemp = [3900, 2500, 1400]
    lentemp = [3850, 2390, 1299]
    coolfact = [0.01, 0.001, 0.001]
    l8 = []
    l10 = []
    l50 = []
    l100 = []
    time8main = []
    time10main = []
    time50main = []
    time100main = []
    for i in range(3):
        init = time.time_ns()
        l8.append(simulated_annealing(data["IA8"], nred, inittemp[i], lentemp[i], coolfact[i]))
        time8 = time.time_ns() - init
        time8main.append(time8)
        print("time8 " + str(i) + " " + str(time8) + " = " + str(time8 / 1000000000) + "s")

        init = time.time_ns()
        l10.append(simulated_annealing(data["IA10"], nred, inittemp[i], lentemp[i], coolfact[i]))
        time10 = time.time_ns() - init
        time10main.append(time10)
        print("time10 " + str(i) + " " + str(time10) + " = " + str(time10 / 1000000000) + "s")

        init = time.time_ns()
        l50.append(simulated_annealing(data["IA50"], nred, inittemp[i], lentemp[i], coolfact[i]))
        time50 = time.time_ns() - init
        time50main.append(time50)
        print("time50 " + str(i) + " " + str(time50) + " = " + str(time50 / 1000000000) + "s")

        init = time.time_ns()
        l100.append(simulated_annealing(data["IA100"], nred, inittemp[i], lentemp[i], coolfact[i]))
        time100 = time.time_ns() - init
        time100main.append(time100)
        print("time100 " + str(i) + " " + str(time100) + " = " + str(time100 / 1000000000) + "s")

        print()

    ret = [{"nred": nred}]
    for i in range(3):
        ret.append({"len": 8, "init_temp": inittemp[i], "templen": lentemp[i], "coolfact": coolfact[i], "size": 8,
                    "times": time8main[i] / 1000000000, "time": time8main[i], "val": sum(l8[i]), "length": len(l8[i]),
                    "list": l8[i]})
    for i in range(3):
        ret.append({"len": 10, "init_temp": inittemp[i], "templen": lentemp[i], "coolfact": coolfact[i], "size": 10,
                    "times": time10main[i] / 1000000000, "time": time10main[i], "val": sum(l10[i]),
                    "length": len(l10[i]), "list": l10[i]})
    for i in range(3):
        ret.append({"len": 50, "init_temp": inittemp[i], "templen": lentemp[i], "coolfact": coolfact[i], "size": 50,
                    "times": time50main[i] / 1000000000, "time": time50main[i], "val": sum(l50[i]),
                    "length": len(l50[i]), "list": l50[i]})
    for i in range(3):
        ret.append({"len": 100, "init_temp": inittemp[i], "templen": lentemp[i], "coolfact": coolfact[i], "size": 100,
                    "times": time100main[i] / 1000000000, "time": time100main[i], "val": sum(l100[i]),
                    "length": len(l100[i]), "list": l100[i]})

    file = open("result_annealing.txt", "w")
    json.dump(ret,file)
    #file.write(str(ret))
    file.close()
    print("finish")
