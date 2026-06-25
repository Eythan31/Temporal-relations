import time
import random
import matplotlib.pyplot as plt
import numpy as np
from periods import *

############################################################################
############################### List of relations ##########################
############################################################################
all_relations = ["0", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", \
                 "5", "6a", "6b", "7a", "7b", "8a", "8b", "9a", "9b", \
                 "10", "11", "12a", "12b", "13a", "13b", "14a", "14b", "15"]

############################################################################
####################### Conditions defining the relations ##################
############################################################################
# dictionary giving the function testing a given temporal relation, given two Period objects
condition = {} 
condition["0"]   = lambda a,b: True
condition["1a"]  = lambda a,b: a.start <= b.end
condition["1b"]  = lambda a,b: a.end >= b.start
condition["2a"]  = lambda a,b: a.start <= b.start
condition["2b"]  = lambda a,b: a.start >= b.start
condition["3a"]  = lambda a,b: a.end <= b.end
condition["3b"]  = lambda a,b: a.end >= b.end
condition["4a"]  = lambda a,b: a.end <= b.start
condition["4b"]  = lambda a,b: a.start >= b.end
condition["5"]   = lambda a,b: a.start <= b.end and a.end >= b.start
condition["6a"]  = lambda a,b: a.start >= b.start and a.start <= b.end
condition["6b"]  = lambda a,b: a.start <= b.start and a.end >= b.start
condition["7a"]  = lambda a,b: a.end >= b.start and a.end <= b.end
condition["7b"]  = lambda a,b: a.start <= b.end and a.end >= b.end
condition["8a"]  = lambda a,b: a.start <= b.start   \
                               and a.end >= b.start \
                               and a.end <= b.end
condition["8b"]  = lambda a,b: b.start <= a.start   \
                               and b.end >= a.start \
                               and b.end <= a.end
condition["9a"]  = lambda a,b: a.start <= b.start and a.end >= b.end
condition["9b"]  = lambda a,b: b.start <= a.start and b.end >= a.end
condition["10"]  = lambda a,b: a.start == b.start
condition["11"]  = lambda a,b: a.end == b.end
condition["12a"] = lambda a,b: a.end == b.start
condition["12b"] = lambda a,b: a.start == b.end
condition["13a"] = lambda a,b: a.start == b.start and a.end <= b.end
condition["13b"] = lambda a,b: a.start == b.start and a.end >= b.end
condition["14a"] = lambda a,b: a.end == b.end and a.start >= b.start
condition["14b"] = lambda a,b: a.end == b.end and a.start <= b.start
condition["15"]  = lambda a,b: a.start == b.start and a.end == b.end

################################
# Algorithm 1: topological order
################################
def alg1(a,b): # a and b are Period objects        
    for relation in reversed(all_relations):
        if condition[relation](a,b):
            return relation

########################################
# Algorithm 2a: DFS-based graph traversal
########################################
# dictionary giving the neighbors of each node of the inverted DAG
graph = {} 
graph["0"]   = ["1a", "1b"]             # "no relation"
graph["1a"]  = ["2a", "3a", "5"]        # "starts before or at end of"
graph["1b"]  = ["5", "3b", "2b"]        # "ends after or at start of"
graph["2a"]  = ["4a", "6b"]             # "starts bef. or at start of"
graph["2b"]  = ["6a", "4b"]             # "starts aft. or at start of"
graph["3a"]  = ["4a", "7a"]             # "ends before or at end of"
graph["3b"]  = ["7b", "4b"]             # "ends after or at end of"
graph["4a"]  = ["12a"]                  # "ends before or at start of"
graph["4b"]  = ["12b"]                  # "starts after or at end of"
graph["5"]   = ["6b", "7a", "7b", "6a"] # "contemporary"
graph["6a"]  = ["10", "9b", "8b"]       # "starts during"
graph["6b"]  = ["8a", "9a", "10"]       # "includes start of"
graph["7a"]  = ["8a", "11", "9b"]       # "ends during"
graph["7b"]  = ["9a", "11", "8b"]       # "includes end of"
graph["8a"]  = ["12a", "14b", "13a"]    # "overlaps before"
graph["8b"]  = ["13b", "14a", "12b"]    # "overlaps after"
graph["9a"]  = ["14b", "13b"]           # "includes"
graph["9b"]  = ["13a", "14a"]           # "included in"
graph["10"]  = ["13a", "13b"]           # "equal start"
graph["11"]  = ["14b", "14a"]           # "equal end"
graph["12a"] = []                       # "meets"
graph["12b"] = []                       # "met by"
graph["13a"] = ["15"]                   # "begins"
graph["13b"] = ["15"]                   # "begun by"
graph["14a"] = ["15"]                   # "ends"
graph["14b"] = ["15"]                   # "ended by"
graph["15"]  = []                       # "equal"

def DFS(node, a, b, marked): # helper function (Depth-First Search)
    if not marked[node]:
        marked[node] = True
        if not condition[node](a,b):
            return None
        for neighbor in graph[node]:
            rel = DFS(neighbor, a, b, marked)
            if rel is not None:
                return rel
        return node
    return None

def alg2a(a, b): # main function (a and b are Period objects)
    return DFS("0", a, b, {rel:False for rel in all_relations})

#############################
# Algorithm 2b: tree traversal
#############################
# dictionary giving the neighbors of each node (list of strings)
tree = {} 
tree["0"]   = ["1a", "1b"]       # "no relation"
tree["1a"]  = ["2a", "3a", "5"]  # "starts before or at end of"
tree["1b"]  = ["3b", "2b"]       # "ends after or at start of"
tree["2a"]  = ["4a", "6b"]       # "starts before or at start of"
tree["2b"]  = []                 # "starts after or at start of"
tree["3a"]  = ["7a"]             # "ends before or at end of"
tree["3b"]  = ["4b"]             # "ends after or at end of"
tree["4a"]  = ["12a"]            # "ends before or at start of"
tree["4b"]  = []                 # "starts after or at end of"
tree["5"]   = ["7b", "6a"]       # "contemporary"
tree["6a"]  = []                 # "starts during"
tree["6b"]  = ["8a", "9a", "10"] # "includes start of"
tree["7a"]  = ["11", "9b"]       # "ends during"
tree["7b"]  = ["8b"]             # "includes end of"
tree["8a"]  = ["14b", "13a"]     # "overlaps before"
tree["8b"]  = ["12b"]            # "overlaps after"
tree["9a"]  = ["13b"]            # "includes"
tree["9b"]  = []                 # "included in"
tree["10"]  = []                 # "equal start"
tree["11"]  = ["14a"]            # "equal end"
tree["12a"] = []                 # "meets"
tree["12b"] = []                 # "met by"
tree["13a"] = []                 # "begins"
tree["13b"] = []                 # "begun by"
tree["14a"] = []                 # "ends"
tree["14b"] = ["15"]             # "ended by"
tree["15"]  = []                 # "equal"

# dictionary giving the function testing a given temporal relation, given two Period objects
condition_short        = {} 
condition_short["0"]   = lambda a,b: True
condition_short["1a"]  = lambda a,b: a.start <= b.end
condition_short["1b"]  = lambda a,b: a.end >= b.start
condition_short["2a"]  = lambda a,b: a.start <= b.start
condition_short["2b"]  = lambda a,b: a.start >= b.start
condition_short["3a"]  = lambda a,b: a.end <= b.end
condition_short["3b"]  = lambda a,b: a.end >= b.end
condition_short["4a"]  = lambda a, b: a.end <= b.start
condition_short["4b"]  = lambda a, b: a.start >= b.end
condition_short["5"]   = lambda a,b: a.end >= b.start
condition_short["6a"]  = lambda a,b: a.start >= b.start
condition_short["6b"]  = lambda a,b: a.end >= b.start
condition_short["7a"]  = lambda a,b: a.end >= b.start
condition_short["7b"]  = lambda a,b: a.end >= b.end
condition_short["8a"]  = lambda a,b: a.end <= b.end
condition_short["8b"]  = lambda a,b: b.start <= a.start
condition_short["9a"]  = lambda a,b: a.end >= b.end
condition_short["9b"]  = lambda a,b: b.start <= a.start
condition_short["10"]  = lambda a,b: a.start == b.start
condition_short["11"]  = lambda a,b: a.end == b.end
condition_short["12a"] = lambda a,b: a.end == b.start
condition_short["12b"] = lambda a,b: a.start == b.end
condition_short["13a"] = lambda a,b: a.start == b.start
condition_short["13b"] = lambda a,b: a.start == b.start
condition_short["14a"] = lambda a,b: a.start >= b.start
condition_short["14b"] = lambda a,b: a.end == b.end
condition_short["15"]  = lambda a,b: a.start == b.start

def tree_traversal(node, a, b): # a and b are Period objects
    if not condition_short[node](a, b):
        return None
    for neighbor in tree[node]:
        rel = tree_traversal(neighbor, a, b)
        if rel is not None:
            return rel
    return node

def alg2b(a, b):  # Algorithm 2b: tree traversal short
    return tree_traversal("0", a, b)

######################################
# Algorithm 2c: explicit decision tree
######################################
def alg2c(a, b): # a and b are Period objects
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


