import json
import random
import time

from basicfunctions import loaddata, add_el, rem_el, rem_2el


def local_search(data, max_same):
    curr_list = data + []
    curr_val = sum(data)
    same = 0
    while same < max_same:
        # print("curr val "+str(sum(curr_list)))
        # print("curr list "+str(curr_list))
        better = False
        rem_list = rem_el(curr_list, data)
        add_list = add_el(curr_list, data)
        neig = rem_list + add_list
        for n in neig:
            if abs(sum(n)) < abs(curr_val):
                curr_list = n
                curr_val = sum(n)
                same = 0
                better = True
            if abs(sum(n)) == abs(curr_val):
                curr_list = n
                curr_val = sum(n)
        if not better:
            neig = rem_2el(curr_list, data)
            for n in neig:
                if abs(sum(n)) < abs(curr_val):
                    curr_list = n
                    curr_val = sum(n)
                    same = 0
                    better = True
                if abs(sum(n)) == abs(curr_val):
                    curr_list = n
                    curr_val = sum(n)
            if not better:
                same = same + 1
    return curr_list


if __name__ == '__main__':
    data = loaddata("data.json")
    init = time.process_time_ns()
    l8 = local_search(data['IA8'], 300)
    time8 = time.process_time_ns() - init
    print(time.process_time_ns())
    print(init)
    print(time8)
    init = time.process_time_ns()
    l10 = local_search(data['IA10'], 300)
    time10 = time.process_time_ns() - init
    print(time10)
    init = time.process_time_ns()
    l50 = local_search(data['IA50'], 300)
    time50 = time.process_time_ns() - init
    print(time50)
    init = time.process_time_ns()
    l100 = local_search(data['IA100'], 300)
    time100 = time.process_time_ns() - init
    print(time100)
    ret = [{"size": 8, "time": time8, "times": time8 / 1000000000, "val": sum(l8), "length": len(l8), "list": l8},
           {"size": 10, "time": time10, "times": time10 / 1000000000, "val": sum(l10), "length": len(l10), "list": l10},
           {"size": 50, "time": time50, "times": time50 / 1000000000, "val": sum(l50), "length": len(l50), "list": l50},
           {"size": 100, "time": time100, "times": time100 / 1000000000, "val": sum(l100), "length": len(l100),
            "list": l100}]

    file = open("result_neighborhood.txt", "w")
    json.dump(ret,file)
    #file.write(str(ret))
    #file.write("\r\n")
    # file.write("Tns10/Tns8="+str(time10/time8))
    file.close()
