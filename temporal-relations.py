import time
import random
import matplotlib.pyplot as plt
import numpy as np

################################################################
########################### DATA MODEL #########################
################################################################

# Class representing a boundary, i.e. the start or end of a Period.
# Usage: Boundary() #For boundaries without any data.
#        Boundary(lb=1914) #For a lower bound ("terminus post quem")
#        Boundary(ub=1918) #For an upper bound ("terminus ante quem")
#        Boundary(1914, 1918) #For a range (lower and upper bounds)
#        Boundary(1914, 1914) #For an exact date
# TODO: try and have a way to write Boundary(1914) for an exact value (and still keep ub and lb named parameters).
class Boundary:
    def __init__(self, lb=None, ub=None):
        if lb is not None and ub is not None and lb > ub:
            raise ValueError("Lower bound cannot exceed upper bound")
        self.lb = lb # lower bound
        self.ub = ub # upper bound

    def __eq__(self, other): #equals operator
        return (self.lb is not None and self.ub is not None
                and self.lb == other.lb and self.ub == other.ub) #check if works for None values

    def __le__(self, other): #lower or equal operator
        return (self.ub is not None and other.lb is not None
                and self.ub <= other.lb)

    def __ge__(self, other): #greater or equal operator
        return (self.lb is not None and other.ub is not None
                and self.lb >= other.ub)

    def __str__(self):
        if self.lb == self.ub:
            return str(self.lb)
        else:
            return "[" + str(self.lb) + "," + str(self.ub) + "]"

    def __repr__(self):
        return self.__str__()

class After(Boundary):
    def __init__(self, lb):
        self.lb = lb
        self.ub = None

class Before(Boundary):
    def __init__(self, ub):
        self.lb = None
        self.ub = ub

class Range(Boundary):
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

# Class representing a time-period (a.k.a. "time-interval").
class Period:
    def __init__(self, start=None, end=None):
        #print("building period, parameters: start=", start, ", end=", end)
        if start is None:
            start = Boundary()
        if end is None:
            end = Boundary()
        if isinstance(start, int):
            self.start = Boundary(start, start)
        else:
            self.start = start
        if isinstance(end, int):
            self.end = Boundary(end, end)
        else:
            self.end = end
        #Need to do a "pre-tightening" for the algorithm to work (ex: to avoid 2a is true but 1a is false)
        # Ensure that the end's lower bound is at least the start's lower bound
        if self.start.lb is not None and \
                (self.end.lb is None or self.end.lb < self.start.lb):
            self.end.lb = self.start.lb
        # Ensure that the start's upper bound is at most the ends's upper bound
        if self.end.ub is not None and \
               (self.start.ub is None or self.start.ub > self.end.ub):
            self.start.ub = self.end.ub

    def __str__(self):
        return "{start=" + str(self.start) \
            + ", end=" + str(self.end) + "}"

    def __repr__(self):
        return self.__str__()

def examples():
    print(Period())  # Unknown boundaries
    print(Period(start=1)) # Known boundary (start)
    print(Period(end=2)) # Known boundary (end)
    print(Period(start=Range(1, 3)))
    print(Period(end=Before(1)))  # Terminus ante quem (on end)
    print(Period(start=After(2)))  # Terminus ante quem (on end)
    print(Period(1914, 1918))  # Known start and end
    print(Period(Boundary(1, 3), Boundary(2, 4))) # Ranges for start and end

############################################################################
############################### Relations ##################################
############################################################################
all_relations = ["0", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", \
                 "5", "6a", "6b", "7a", "7b", "8a", "8b", "9a", "9b", \
                 "10", "11", "12a", "12b", "13a", "13b", "14a", "14b", "15"]

condition = {} # dictionary giving the function testing a given temporal relation, given two Period objects
condition["0"] = lambda a,b: True
condition["1a"] = lambda a,b: a.start <= b.end
condition["1b"] = lambda a,b: a.end >= b.start
condition["2a"] = lambda a,b: a.start <= b.start
condition["2b"] = lambda a,b: a.start >= b.start
condition["3a"] = lambda a,b: a.end <= b.end
condition["3b"] = lambda a,b: a.end >= b.end
condition["4a"] = lambda a,b: a.end <= b.start
condition["4b"] = lambda a,b: a.start >= b.end
condition["5"]  = lambda a,b: a.start <= b.end and a.end >= b.start
condition["6a"] = lambda a,b: a.start >= b.start and a.start <= b.end
condition["6b"] = lambda a,b: a.start <= b.start and a.end >= b.start
condition["7a"] = lambda a,b: a.end >= b.start and a.end <= b.end
condition["7b"] = lambda a,b: a.start <= b.end and a.end >= b.end
condition["8a"] = lambda a,b: a.start <= b.start and a.end >= b.start and a.end <= b.end
condition["8b"] = lambda a,b: b.start <= a.start and b.end >= a.start and b.end <= a.end
condition["9a"] = lambda a,b: a.start <= b.start and a.end >= b.end
condition["9b"] = lambda a,b: b.start <= a.start and b.end >= a.end
condition["10"]  = lambda a,b: a.start == b.start
condition["11"]  = lambda a,b: a.end == b.end
condition["12a"] = lambda a,b: a.end == b.start
condition["12b"] = lambda a,b: a.start == b.end
condition["13a"] = lambda a,b: a.start == b.start and a.end <= b.end
condition["13b"] = lambda a,b: a.start == b.start and a.end >= b.end
condition["14a"] = lambda a,b: a.end == b.end and a.start >= b.start
condition["14b"] = lambda a,b: a.end == b.end and a.start <= b.start
condition["15"] = lambda a,b: a.start == b.start and a.end == b.end

################################
# Algorithm 1: topological order
################################
def alg1(a,b): # Breadth traversal, from above to below (topological order)
    for relation in reversed(all_relations):
        if condition[relation](a,b):
            return relation

########################################
# Algorithm 2: DFS-based graph traversal
########################################
# IMPLICATION GRAPH (inverted))
graph = {} # dictionary giving the neighbors of each node (list of strings)
graph["0"]  = ["1a", "1b"]
graph["1a"] = ["2a", "3a", "5"] # "starts before or at end of"
graph["1b"] = ["5", "3b", "2b"] # "ends after or at start of"
graph["2a"] = ["4a", "6b"] # "starts before or at start of"
graph["2b"] = ["6a", "4b"] # "starts after or at start of"
graph["3a"] = ["4a", "7a"] # "ends before or at end of"
graph["3b"] = ["7b", "4b"] # "ends after or at end of"
graph["4a"] = ["12a"] # "ends before or at start of"
graph["4b"] = ["12b"] # "starts after or at end of"
graph["5"]  = ["6b", "7a", "7b", "6a"] # "contemporary"
graph["6a"] = ["10", "9b", "8b"] # "starts during"
graph["6b"] = ["8a", "9a", "10"] # "includes start of"
graph["7a"] = ["8a", "11", "9b"] # "ends during"
graph["7b"] = ["9a", "11", "8b"] # "includes end of"
graph["8a"] = ["12a", "14b", "13a"] # "overlaps before"
graph["8b"] = ["13b", "14a", "12b"] # "overlaps after"
graph["9a"] = ["14b", "13b"] # "includes"
graph["9b"] = ["13a", "14a"] # "included in"
graph["10"]  = ["13a", "13b"] # "equal start"
graph["11"]  = ["14b", "14a"] # "equal end"
graph["12a"] = [] # "meets"
graph["12b"] = [] # "met by"
graph["13a"] = ["15"] # "begins"
graph["13b"] = ["15"] # "begun by"
graph["14a"] = ["15"] # "ends"
graph["14b"] = ["15"] # "ended by"
graph["15"] = [] # equal

marked = {}
marked = dict((rel, False) for rel in all_relations)

def init_dict(dictionary, value):
    for key in dictionary:
        dictionary[key] = value

def DFS_alg2(node, a, b): #DFS, full conditions, not marking successors (returning the relation)
    if not marked[node]:
        marked[node] = True
        if not condition[node](a,b):
            return None
        for neighbor in graph[node]:
            rel = DFS_alg2(neighbor, a, b)
            if rel is not None:
                return rel
        return node
    return None

def alg2(a, b): # Algorithm 2: depth-first search in the graph
    init_dict(marked, False)
    return DFS_alg2("0", a, b)

########################################################
# Algorithm 3: tree traversal (with reduced conditions)
########################################################
tree = {} # dictionary giving the neighbors of each node (list of strings)
tree["0"]  = ["1a", "1b"]
tree["1a"] = ["2a", "3a", "5"] # "starts before or at end of"
tree["1b"] = ["3b", "2b"] # "ends after or at start of"
tree["2a"] = ["4a", "6b"] # "starts before or at start of"
tree["2b"] = [] # "starts after or at start of"
tree["3a"] = ["7a"] # "ends before or at end of"
tree["3b"] = ["4b"] # "ends after or at end of"
tree["4a"] = ["12a"] # "ends before or at start of"
tree["4b"] = [] # "starts after or at end of"
tree["5"]  = ["7b", "6a"] # "contemporary"
tree["6a"] = [] # "starts during"
tree["6b"] = ["8a", "9a", "10"] # "includes start of"
tree["7a"] = ["11", "9b"] # "ends during"
tree["7b"] = ["8b"] # "includes end of"
tree["8a"] = ["14b", "13a"] # "overlaps before"
tree["8b"] = ["12b"] # "overlaps after"
tree["9a"] = ["13b"] # "includes"
tree["9b"] = [] # "included in"
tree["10"]  = [] # "equal start"
tree["11"]  = ["14a"] # "equal end"
tree["12a"] = [] # "meets"
tree["12b"] = [] # "met by"
tree["13a"] = [] # "begins"
tree["13b"] = [] # "begun by"
tree["14a"] = [] # "ends"
tree["14b"] = ["15"] # "ended by"
tree["15"] = [] # equal

condition_short = {} # dictionary giving the function testing a given temporal relation, given two Period objects
condition_short["0"] = lambda a,b: True
condition_short["1a"] = lambda a,b: a.start <= b.end
condition_short["1b"] = lambda a,b: a.end >= b.start
condition_short["2a"] = lambda a,b: a.start <= b.start
condition_short["2b"] = lambda a,b: a.start >= b.start
condition_short["3a"] = lambda a,b: a.end <= b.end
condition_short["3b"] = lambda a,b: a.end >= b.end
condition_short["4a"] = lambda a, b: a.end <= b.start
condition_short["4b"] = lambda a, b: a.start >= b.end
condition_short["5"]  = lambda a,b: a.end >= b.start
condition_short["6a"] = lambda a,b: a.start >= b.start
condition_short["6b"] = lambda a,b: a.end >= b.start
condition_short["7a"] = lambda a,b: a.end >= b.start
condition_short["7b"] = lambda a,b: a.end >= b.end
condition_short["8a"] = lambda a,b: a.end <= b.end
condition_short["8b"] = lambda a,b: b.start <= a.start
condition_short["9a"] = lambda a,b: a.end >= b.end
condition_short["9b"] = lambda a,b: b.start <= a.start
condition_short["10"]  = lambda a,b: a.start == b.start
condition_short["11"]  = lambda a,b: a.end == b.end
condition_short["12a"] = lambda a,b: a.end == b.start
condition_short["12b"] = lambda a,b: a.start == b.end
condition_short["13a"] = lambda a,b: a.start == b.start
condition_short["13b"] = lambda a,b: a.start == b.start
condition_short["14a"] = lambda a,b: a.start >= b.start
condition_short["14b"] = lambda a,b: a.end == b.end
condition_short["15"] = lambda a,b: a.start == b.start

def tree_traversal_short(node, a, b):
    if not condition_short[node](a, b):
        return None
    for neighbor in tree[node]:
        rel = tree_traversal_short(neighbor, a, b)
        if rel is not None:
            return rel
    return node

def alg3(a, b):  # Algorithm 3b: tree traversal short
    return tree_traversal_short("0", a, b)

#####################################
# Algorithm 4: explicit decision tree
#####################################
def alg4(a, b): #explicit decision tree
    if a.start <= b.end:
        if a.start <= b.start:
            if a.end <= b.start:
                if a.end == b.start:
                    return "12a"
                return "4a"
            if a.end >= b.start:
                if b.end >= a.end:
                    if b.end == a.end:
                        if a.start == b.start:
                            return "15"
                        return "14b"
                    if a.start == b.start:
                        return "13a"
                    return "8a"
                if a.end >= b.end:
                    if a.start == b.start:
                        return "13b"
                    return "9a"
                if a.start == b.start:
                    return "10"
                return "6b"
            return "2a"
        if a.end <= b.end:
            if a.end >= b.start:
                if a.end == b.end:
                    if a.start >= b.start:
                        return "14a"
                    return "11"
                if a.start >= b.start:
                    return "9b"
                return "7a"
            return "3a"
        if a.end >= b.start:
            if a.end >= b.end:
                if a.start >= b.start:
                    if a.start == b.end:
                        return "12b"
                    return "8b"
                return "7b"
            if a.start >= b.start:
                return "6a"
            return "5"
        return "1a"
    if a.end >= b.start:
        if a.end >= b.end:
            if a.start >= b.end:
                return "4b"
            return "3b"
        if a.start >= b.start:
            return "2b"
        return "1b"
    return "0"

############################################################################
############################### TEST FUNCTIONS #############################
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

def validate_algorithms(algs, alg_names):
    i = 0
    for alg in algs:
        for relation in all_relations:
            if (result := alg(*test[relation])) != relation:
                print("%s on relation %s failed, returned %s" % (alg_names[i], relation, result))
                return False
        print("%s validated" % alg_names[i])
        i = i+1
    return True

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
# Data examples
print("Data examples:")
examples()

# Validation of the algorithms
print("\nValidation (testing) of algorithms:")
algs = [alg1, alg2, alg3, alg4]
alg_names = ["alg. 1", "alg. 2", "alg. 3", "alg. 4"]
validated = validate_algorithms(algs, alg_names)
print("Validating algorithms... %s" % " validated." if validated else "NOT validated.")

# Measuring general execution times of each algorithm
print("\nGeneral execution times:")
SEED = 17
N = 1000000
test_general_execution_times(N, algs, alg_names, SEED)

# Measuring general execution times per relation
print("\nExecution times by relation:")
N = 100000
times = test_by_relation(N, algs, alg_names)
