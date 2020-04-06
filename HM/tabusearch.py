import time,json

from basicfunctions import loaddata, add_el, rem_el, rem_2el


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


def tabu_search(data_set):
    best_sol = data_set
    hist = []
    count = 0
    short_tabu_steps = 3
    hist.append([short_tabu_steps, best_sol])
    same = 0
    next_sol = det_x_next(hist, best_sol, data_set)
    prev_sol = best_sol
    prev_sols = [best_sol]
    intermediate_sol = [best_sol]
    while same < 10:

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
    init = time.time_ns()
    l8 = tabu_search(data['IA8'])
    time8 = time.time_ns() - init
    print(l8)
    print(sum(l8))
    print("time8 " + str(time8) + " = " + str(time8 / 1000000000) + "s")

    init = time.time_ns()
    l10 = tabu_search(data['IA10'])
    time10 = time.time_ns() - init
    print(l10)
    print(sum(l10))
    print("time10 " + str(time10) + " = " + str(time10 / 1000000000) + "s")
    
    init = time.time_ns()
    l50 = tabu_search(data['IA50'])
    time50 = time.time_ns() - init
    print(l50)
    print(sum(l50))
    print("time50 " + str(time50) + " = " + str(time50 / 1000000000) + "s")

    init = time.time_ns()
    l100 = tabu_search(data['IA100'])
    time100 = time.time_ns() - init
    print(l100)
    print(sum(l100))
    print("time100 " + str(time100) + " = " + str(time100 / 1000000000) + "s")
    
    ret = [{"size": 8, "time": time8, "times": time8 / 1000000000, "val": sum(l8), "length": len(l8), "list": l8},
           {"size": 10, "time": time10, "times": time10 / 1000000000, "val": sum(l10), "length": len(l10), "list": l10},
           {"size": 50, "time": time50, "times": time50 / 1000000000, "val": sum(l50), "length": len(l50), "list": l50},
           {"size": 100, "time": time100, "times": time100 / 1000000000, "val": sum(l100), "length": len(l100),
            "list": l100}]
    
    file = open("result_tabu.txt", "w")
    json.dump(ret,file)
    #file.write(str(ret))
    file.close()
    print("finish")
