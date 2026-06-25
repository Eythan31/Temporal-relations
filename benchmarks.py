import time
import random
import matplotlib.pyplot as plt
import numpy as np
from periods import *
from algorithms import *

############################################################################
############################### Test data ##################################
############################################################################
test = {}
test["0"]   = (Period(), Period())
test["1a"]  = (Period(start=1), Period(end=2))
test["1b"]  = tuple(reversed(test["1a"]))
test["2a"]  = (Period(start=1), Period(start=2))
test["2b"]  = tuple(reversed(test["2a"]))
test["3a"]  = (Period(end=1), Period(end=2))
test["3b"]  = tuple(reversed(test["3a"]))
test["4a"]  = (Period(end=1), Period(start=2))
test["4b"]  = tuple(reversed(test["4a"]))
test["5"]   = (Period(Before(1), After(2)), Period(Before(1), After(2)))
test["6a"]  = (Period(start=2), Period(1, 3))
test["6b"]  = tuple(reversed(test["6a"]))
test["7a"]  = (Period(end=2), Period(1, 3))
test["7b"]  = tuple(reversed(test["7a"]))
test["8a"] = (Period(1, 3), Period(2, 4))
test["8b"] = tuple(reversed(test["8a"]))
test["9a"] = (Period(1, 4), Period(2, 3))
test["9b"] = tuple(reversed(test["9a"]))
test["10"]   = (Period(start=1), Period(start=1))
test["11"]   = (Period(end=1), Period(end=1))
test["12a"] = (Period(1, 2), Period(2, 3))
test["12b"] = tuple(reversed(test["12a"]))
test["13a"] = (Period(1, 2), Period(1, 3))
test["13b"] = tuple(reversed(test["13a"]))
test["14a"] = (Period(2, 3), Period(1, 3))
test["14b"] = tuple(reversed(test["14a"]))
test["15"]  = (Period(1, 2), Period(1, 2))

############################################################################
############################### Testing functions ##########################
############################################################################
algs = [alg1, alg2a, alg2b, alg2c]
alg_names = ["alg. 1", "alg. 2a", "alg. 2b", "alg. 2c"]

def test_random(N, alg, start=0, end=len(all_relations)):
    for i in range(N):
        random_relation = all_relations[random.randrange(start, end)]
        alg(*test[random_relation])

def test_random_N_times(N, algorithms, alg_names, seed=10, start=0, end=len(all_relations)):
    times = []
    i = 0
    for alg in algorithms:
        random.seed(seed)
        start_time = time.time()
        test_random(N, alg, start, end)
        end_time = round(time.time() - start_time, 2)
        times.append(end_time)
        print("Testing %s : --- %s seconds ---" % (alg_names[i], end_time))
        i = i+1
    return times

def test_general_execution_times(N, algs, alg_names, SEED):
    times = test_random_N_times(N, algs, alg_names, SEED)
    x = range(len(times))
    bars = plt.bar(x, times)
    tick_labels = alg_names
    plt.xticks(x, tick_labels, fontsize=11)
    plt.ylabel("Execution time (seconds)", fontsize=11)
    plt.xlabel("Algorithm", fontsize=11)
    i = 0
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 times[i], ha='center', va='bottom', fontsize=11)
        i = i + 1
    plt.show()

def test_by_relation(N, algs, alg_names):
    PRECISION = 3
    times = {}
    i = 0
    for alg in algs:
        for relation in all_relations:
            start_time = time.time()
            for j in range(N):
                alg(*test[relation])
            end_time = round(time.time() - start_time, PRECISION)
            times[(alg_names[i], relation)] = end_time
        i = i+1

    fig, ax = plt.subplots()
    for alg in alg_names:
        plt.plot(np.array([times[(alg, relation)] for relation in all_relations]), label=alg)
        ax.set_xticks(range(0, 27))
        ax.set_xticklabels(all_relations, rotation=90, ha='right')
    print()
    plt.ylabel("Execution time (seconds)", fontsize=11)
    plt.xlabel("Relation", fontsize=11)
    ax.legend()
    plt.show()

############################################################################
############################### MAIN #######################################
############################################################################

# Measuring general execution times of each algorithm
print("\nGeneral execution times:")
SEED = 17
N = 1000000
test_general_execution_times(N, algs, alg_names, SEED)

# Measuring general execution times per relation
print("\nExecution times by relation:")
N = 100000
times = test_by_relation(N, algs, alg_names)
