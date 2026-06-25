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
############################### Validation functions #######################
############################################################################
algs = [alg1, alg2a, alg2b, alg2c]
alg_names = ["alg. 1", "alg. 2a", "alg. 2b", "alg. 2c"]

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

############################################################################
############################### MAIN #######################################
############################################################################

print("\nValidation (testing) of algorithms:")
algs = [alg1, alg2a, alg2b, alg2c]
alg_names = ["alg. 1", "alg. 2a", "alg. 2b", "alg. 2c"]
validated = validate_algorithms(algs, alg_names)
print("Validating algorithms... %s" % " validated." if validated else "NOT validated.")
