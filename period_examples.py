from periods import *

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
############################### MAIN #######################################
############################################################################
print("Period examples:")
examples()
