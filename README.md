# Temporal-relations

Source code for the article "Detecting Temporal Relations in Archaeology: Model and Algorithms", by Eythan Levy (preprint under review). The article presents algorithms for automated detection of temporal relations between temporal intervals featuring uncertainties (ranges) on their boundaries. The temporal relations are based on the system devised in [Levy 2025](https://doi.org/10.1111/arcm.13080). The algorithms are implemented in the Python language. The preprint is available on HAL: [https://hal.science/hal-05210722v1](https://hal.science/hal-05210722v1). 
This repository contains the following files:
	-periods.py: our main data structure, a time-period (a.k.a., time-interval) containing two boundaries (start and end).
	-period_examples.py: examples of usage of the class Period.
	-algorithms.py: our four algorithms for detecting the strongest temporal relation between two time-periods.
	-temporal-relations-examples.py: examples of strongest temporal relations.
	-validate-algorithms.py: test cases for our four algorithms.
	-benchmarks.py: comparison of execution speeds of our four algorithms (section 4.3 in the paper).
	-case-study.py: source code for our case study (section 6 in the paper).
	-case-study.clog: ChronoLog file used to generate the Directed Acyclical Graph (DAG) of the case study (fig. 9 in the paper). 