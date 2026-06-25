###########################################################################
# Class representing a boundary, i.e. the start or end of a Period.
# Usage: Boundary()           #For boundaries without any data.
#        Boundary(lb=1914)    #For a lower bound ("terminus post quem")
#        Boundary(ub=1918)    #For an upper bound ("terminus ante quem")
#        Boundary(1914, 1918) #For a range (lower and upper bounds)
#        Boundary(1914, 1914) #For an exact date
###########################################################################
class Boundary:
    def __init__(self, lb=None, ub=None):
        if lb is not None and ub is not None and lb > ub:
            raise ValueError("Lower bound cannot exceed upper bound")
        self.lb = lb # lower bound
        self.ub = ub # upper bound

    def __eq__(self, other): # equals operator  
        return (self.lb is not None and self.ub is not None
                and self.lb == other.lb and self.ub == other.ub)  

    def __le__(self, other): # lower or equal operator
        return (self.ub is not None and other.lb is not None
                and self.ub <= other.lb)

    def __ge__(self, other): # greater or equal operator
        return (self.lb is not None and other.ub is not None
                and self.lb >= other.ub)

    def __str__(self): # conversion to string
        if self.lb == self.ub: # known value
            return str(self.lb)
        else:
            return "[" + str(self.lb) + "," + str(self.ub) + "]"

    def __repr__(self): # for printing
        return self.__str__()

class After(Boundary): # Terminus Post Quem
    def __init__(self, lb):
        self.lb = lb
        self.ub = None

class Before(Boundary): # Terminus Ante Quem
    def __init__(self, ub):
        self.lb = None
        self.ub = ub

class Range(Boundary): # Range
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

###########################################################################
# Class representing a time-period (a.k.a. "time-interval"), consisting of
# two boundaries.
###########################################################################
class Period:
    def __init__(self, start=None, end=None):
        # Initialize start
        if start is None:
            self.start = Boundary()
        elif isinstance(start, int):
            self.start = Boundary(start, start)
        elif isinstance(start, Boundary):
            self.start = start
        else:
            raise ValueError("Wrong start: use None, int or Boundary")

        # Initialize end
        if end is None:
            self.end = Boundary()
        elif isinstance(end, int):
            self.end = Boundary(end, end)
        elif isinstance(end, Boundary):
            self.end = end
        else:
            raise ValueError("Wrong end: use None, int or Boundary")
        
        # Ensure that the end's lower bound equals at least the 
        # start's lower bound                    
        if self.start.lb is not None and \
                (self.end.lb is None or self.end.lb < self.start.lb):
            self.end.lb = self.start.lb
            
        # Ensure that the start's upper bound equals at most the 
        # ends's upper bound
        if self.end.ub is not None and \
               (self.start.ub is None or self.start.ub > self.end.ub):
            self.start.ub = self.end.ub

    def __str__(self): # conversion to string
        return "{start=" + str(self.start) \
            + ", end=" + str(self.end) + "}"

    def __repr__(self): # for printing
        return self.__str__()

