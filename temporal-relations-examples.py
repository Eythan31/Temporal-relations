from periods import *
from algorithms import *

def test_with_fixed_known_period_B():
    As = {}
    B = Period(2,4)    
    As["0"] = Period(start=Range(1,5), end=Range(1,5))
    As["1a"] = Period(start=Range(1,3), end=Range(1,5))
    As["2a"] = Period(start=1, end=Range(1,5))
    As["3a"] = Period(start=Range(1,4), end=Range(1,4))
    As["4a"] = Period(start=1, end=Range(1,2))
    As["5"] = Period(start=Range(1,3), end=Range(3,5))
    As["6a"] = Period(start=3, end=Range(3,5))
    As["7a"] = Period(start=Range(1,3), end=3)
    As["8a"] = Period(1,3)
    As["9a"] = Period(1,5)
    As["10"] = Period(2,Range(3,5))
    As["11"] = Period(Range(1,3),4)
    As["12a"] = Period(1,2)
    As["13a"] = Period(2,3)
    As["14a"] = Period(3,4)
    As["15"] = Period(2,4)

    for A in As.values():
        print("A:", A)
        print("B:", B)
        print("Strongest relation:")
        print(alg2c(A,B))
        print()

test_with_fixed_known_period_B()
