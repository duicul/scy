import json
import random
import time
import math


def func_map(x):
    return 1 / (1 + math.exp(-x))


def generate(filename):
    f = open(filename, "w")
    data = {}
    sizes = [8, 10, 50, 100]
    delta = 100
    key = ""
    for size in sizes:
        print(size)
        t = [random.randint(-delta, delta) for i in range(size)]
        key = "IA" + str(size)
        data[key] = t
    f.write(json.dumps(data))
    f.close()
    print(data["IA8"])
    print(data["IA10"])


def loaddata(filename):
    f = open(filename, "r")
    data = json.loads(f.read())
    f.close()
    return data


def add_el(curr_sol, sol_space):
    neig = []
    for val in sol_space:
        if val not in curr_sol:
            neig.append(curr_sol + [val])
    return neig


def rem_el(curr_sol, sol_space):
    neig = []
    # print(data_set)
    for val in sol_space:
        # print(val)
        if val in curr_sol:
            aux = [] + curr_sol
            aux.remove(val)
            if not len(aux) == 0:
                neig.append(aux)
    return neig


def rem_2el(curr_sol, sol_space):
    neig = []
    # print(data_set)
    for val in sol_space:
        for val1 in sol_space:
            if not val1 == val:
                # print(val)
                if val in curr_sol and val1 in curr_sol:
                    aux = [] + curr_sol
                    aux.remove(val)
                    aux.remove(val1)
                    if not len(aux) == 0:
                        neig.append(aux)
    return neig


def alfasecond(t, beta):
    return t / (1 + beta * t)
