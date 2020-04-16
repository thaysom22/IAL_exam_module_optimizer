# IAL_exam_module_optimizer

[![Run on Repl.it](https://repl.it/badge/github/thaysom22/IAL_exam_module_optimizer)](https://repl.it/github/thaysom22/IAL_exam_module_optimizer)

Python application to optimize module allocations for Pearson Edexcel International A-Level (IAL) Mathematics and Further Mathematics (2018). 

The purpose of this application is to take a set of module names and results from the user and output how the modules should be allocated to acquire the best grade (A* to E) possible in the A-Level Mathematics and the Further Mathematics (FM) awards. 

The Pearson Edexcel International A-Level Mathematics and Further Mathematics (2018) specification is available as a pdf [here](https://qualifications.pearson.com/en/qualifications/edexcel-international-advanced-levels/mathematics-2018.html). 
Official and complete information regarding module requirements, and UMS (Uniform Mark Scale) boundaries for grades can be found in this document. 

Notes
1. The highest A-level grade is prioritized over the highest FM grade: i.e if there are no valid assignments of completed modules that satisfy the highest possible grade available in each award individually then the FM grade will be reduced and the list of valid assignments recalculated.
2. 





Modules in depository:

main.py
This script calls functions from other modules in repository to implement optimization. Takes input or randomly generates module selection and results and outputs recommended combination and allocation of modules to maximise awarded grades. 

optimization_functions.py
This script contains function definitions of functions which are called in optimize.py script to facilitate objective of the program

imput_functions.py
functions to facilitate user input of data...

tests.py
This script contains tests....

Improvements I would like to make as I learn more skills:
1. Input module results for multiple students and output optimized allocations for each student.


