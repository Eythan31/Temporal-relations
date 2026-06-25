from periods import *
from algorithms import *

############################################################################
############################### Relations names ############################
############################################################################

names = {} # dictionary giving the neighbors of each node (list of strings)
names["0"]  = "None"
names["1a"] = "starts before or at end of"
names["1b"] = "ends after or at start of"
names["2a"] = "starts before or at start of"
names["2b"] = "starts after or at start of"
names["3a"] = "ends before or at end of"
names["3b"] = "ends after or at end of"
names["4a"] = "ends before or at start of"
names["4b"] = "starts after or at end of"
names["5"]  = "contemporary"
names["6a"] = "starts during"
names["6b"] = "includes start of"
names["7a"] = "ends during"
names["7b"] = "includes end of"
names["8a"] = "overlaps before"
names["8b"] = "overlaps after"
names["9a"] = "includes"
names["9b"] = "included in"
names["10"] = "equal start"
names["11"] = "equal end"
names["12a"] = "meets"
names["12b"] = "met by"
names["13a"] = "begins"
names["13b"] = "begun by"
names["14a"] = "ends"
names["14b"] = "ended by"
names["15"] =  "equal"

########
phases = {}
phases["Abu al-Kharaz, EBIB"] = Period(end=Range(-3090, -2940))
phases["Abu al-Kharaz, EBII"] = Period(start=Range(-3090, -2940))
phases["Ashkelon, EBIA"] = Period(end=Range(-3520, -3220))
phases["Ashkelon, EBIB"] = Period(start=Range(-3520, -3220))
phases["Bahb ed-Drah, EBIB"] = Period(end=Range(-3220, -2520))
phases["Bahb ed-Drah, EBII"] = Period(start=Range(-3220, -2520))
phases["Beth Yerah, EBIA"] = Period(end=Range(-3650,-3330))
phases["Beth Yerah, EBII"] = Period(start=Range(-3550, -3120), end=Range(-3190,-2660))
phases["Beth Yerah, EBIII"] = Period(start=Range(-3190,-2660))
phases["Jericho, EBII"] = Period(end=Range(-2990, -2760))
phases["Jericho, EBIII"] = Period(start=Range(-2990, -2760))
phases["Kabri, EBIA"] = Period(end=Range(-3380, -3100))
phases["Kabri, EBIB"] = Period(start=Range(-3380, -3100), end=Range(-3350, -3010))
phases["Kabri, EBII"] = Period(start=Range(-3350, -3010))
phases["Yarmuth, EBIB"] = Period(end=Range(-3050, -2920))
phases["Yarmuth, EBII"] = Period(start=Range(-3050, -2920), end=Range(-3010, -2900))
phases["Yarmuth, EBIII"] = Period(start=Range(-3010, -2900))
phases["Tel el-Umeiri, EBII"] = Period(end=Range(-3090, -2920))
phases["Tel el-Umeiri, EBIII"] = Period(start=Range(-3090, -2920))


############################
# whole matrix
i=1
for a in phases.keys():
    for b in phases.keys():
        print(i, ". (", a,",",b, ")", sep="")
        print("Strongest relation: ", end="")
        strongest = strongest_relation(phases[a], phases[b])
        print(names[strongest], " (",strongest,")", sep="")
        print()
        i+=1
############################
