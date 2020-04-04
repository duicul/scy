import json
import random
import time

from basicfunctions import loaddata


def backtrack(data, mindev, subset):
    auxsubset = subset
    auxmindev = mindev
    for i in data:
        # print("for"+str(i))
        if i not in subset:
            # print("subset"+str(i))
            aux = backtrack(data, i if mindev == None else mindev + i, subset + [i])
            if auxmindev == None or abs(sum(aux)) < auxmindev or (
                    abs(sum(aux)) == auxmindev and len(aux) > len(auxsubset)):
                # print(str(i)+"if"+str(abs(sum(aux))))
                auxsubset = aux
                auxmindev = abs(sum(aux))
    return auxsubset


if __name__ == "__main__":
    data = loaddata("data.json")

    init = time.time_ns()
    l8 = backtrack(data["IA8"], None, [])
    time8 = time.time_ns() - init
    print(l8)

    init = time.time_ns()
    l10 = backtrack(data["IA10"], None, [])
    time10 = time.time_ns() - init
    print(l10)

    ret = []
    ret.append({"size": 8, "time": time8, "times": time8 / 1000000000, "val": sum(l8), "length": len(l8), "list": l8})
    ret.append(
        {"size": 10, "time": time10, "times": time10 / 1000000000, "val": sum(l10), "length": len(l10), "list": l10})

    file = open("result_backtracking.txt", "w")
    file.write(str(ret))
    file.write("\r\n")
    file.write("Tns10/Tns8=" + str(time10 / time8))
    file.close()
