###TODO###
#Add function to optimization_functions to perform A* check for A-level
#Complete README file

import sys


from optimization_functions import *
from input_functions import *

#declare container variables
all_units = ['P1', 'P2', 'P3', 'P4', 'FP1', 'FP2', 'FP3', 'M1', 'M2', 'M3', 'S1', 'S2', 'S3', 'D1']
IAS_units = ['P1', 'P2', 'FP1', 'M1', 'S1', 'D1']
IA2_FM_units_list = ['FP2', 'FP3', 'M2', 'M3', 'S2', 'S3']
A_level_compulsory_units = ['P1', 'P2', 'P3', 'P4']
A_level_optional_units = ['D1', 'M1', 'S1', 'M2', 'S2']
A_level_optional_valid_combos = [['M1', 'M2'], ['S1', 'S2'], ['M1', 'S1'], ['D1', 'S1'], ['D1', 'M1']]
FM_compulsory_valid_combos = [['FP1', 'FP2'], ['FP1', 'FP3']] 
FM_optional_units = ['FP2', 'FP3', 'M1', 'M2', 'M3', 'S1', 'S2', 'S3', 'D1']
grade_boundaries_dict = {'A':480, 'B':420, 'C':360, 'D':300, 'E':240}

while 1:
  
  #Input module results \
  #then perform 'less computationally demanding' initial combinations checks before generating overall space or \
  #available set of combinations
  print('Enter completed module results: ') 
  completed_module_results = input_module_results(all_units)
  print('Completed module results as dict:')
  print(completed_module_results)
  print()
  A_level_combos_check = A_level_module_requirements_check(completed_module_results, A_level_compulsory_units, \
A_level_optional_valid_combos)
  if not A_level_combos_check:
    print('No valid A-level combination is available')
    continue
  print('Valid A-level combination is available')
  #create space of valid combos for A-level by calling function invoking itertools
  A_level_combos_space = overall_combos_A_level_space(A_level_compulsory_units, A_level_optional_valid_combos)
  #generate ordered list of tuples containing available valid combos with totals for A-level
  A_level_available_combos_and_totals = available_combos_ordered(completed_module_results, A_level_combos_space)
  #calculate max possible grade A to E at A-level
  A_level_best_grade = max_grade_A_to_E(A_level_available_combos_and_totals, grade_boundaries_dict)
  if not A_level_best_grade:
    print('Total UMS requirement for A-level minimum grade not met')
    continue
  print('Total UMS requirement for A-level minimum grade met')
  FM_combos_check = FM_module_requirements_check(completed_module_results, FM_compulsory_valid_combos)
  if not FM_combos_check:
    print('No valid FM combination is available')
    #if A_level_best_grade == 'A' then check if A* is awarded
    #print the best possible grade at A-level given the available combinations in completed_module resuts
    #then exit program
    if bool_A_level_A_star(completed_module_results, A_level_best_grade):
      print('A-level: A*')
    else:
      print('A-level: {}'.format(A_level_best_grade))
    A_level_only_max_combo = max_available_overall_combo(A_level_available_combos_and_totals)
    print(A_level_only_max_combo)  
    sys.exit()
  print('Valid FM combination is available')
  break
           
#create spaces of valid combos  by calling functions invoking itertools for FM and FM IA2 units
FM_combos_space = overall_combos_FM_space(FM_compulsory_valid_combos, FM_optional_units)
IA2_FM_combos_space = IA2_FM_units_combos_space(IA2_FM_units_list)

#generate ordered list of tuples containing available valid combos with totals for FM and FM IA2 units
FM_available_combos_and_totals = available_combos_ordered(completed_module_results, FM_combos_space)
IA2_units_available_combos_and_totals = available_combos_ordered(completed_module_results, IA2_FM_combos_space)

#calculate max possible grade A to E at FM
FM_best_grade = max_grade_A_to_E(FM_available_combos_and_totals, grade_boundaries_dict)

#filter A_level_valid_combos_and_totals and FM_valid_combos_and_totals for combos with total satisfying max grade requirement
A_level_best_grade_combos_and_totals = filter_above_total(A_level_available_combos_and_totals, \
grade_boundaries_dict[A_level_best_grade])
FM_best_grade_combos_and_totals =filter_above_total(FM_available_combos_and_totals, grade_boundaries_dict[FM_best_grade])

#filter available combos of IA2 units for only A* combos
IA2_units_available_A_star_combos = filter_above_total(IA2_units_available_combos_and_totals, 270)

#boolean function for True/False A* at FM possible
bool_FM_A_star = bool_FM_A_star(IA2_units_available_A_star_combos, FM_best_grade)

#split program flow by if A* at FM is possible
if bool_FM_A_star:
  #create list of tuples of available overall FM combos that satify A* requirements
  #if bool_FM_A_star boolean function returns 'True' then FM_best_grade_combos_and_totals will contain only A grade combos
  overall_available_FM_A_star_combos = available_overall_A_star_FM_combos\
  (FM_best_grade_combos_and_totals, IA2_units_available_A_star_combo)
  #create list of tuples of available overall combos which satisfy A-level best possible grade and FM A* requirements
  overall_A_level_and_FM_A_star = overall_available_combos_and_totals\
(A_level_best_grade_combos_and_totals, overall_available_FM_A_star_combos)
  #check if there are any available combinations 
  if overall_A_level_and_FM_A_star != []:
    #print the available combo with the highest sum of A-level and FM UMS scores
    max_combo = max_available_overall_combo(overall_A_level_and_FM_A_star)
    if bool_A_level_A_star(completed_module_results, A_level_best_grade):
      print('A-level: A*')
    else:
      print('A-level: {}'.format(A_level_best_grade))
    print('FM: A*')
    print('Overall combo with max sum of overall A-level and overall FM total:')
    print(max_combo)
    print()
    sys.exit()  

#if A* at FM not possible or no combination satisfying A-level best possible grade requirements and FM A* requirements\
#is available then\
#create list of overall module combos and totals that satisfy max possible grade requirements for A level and for FM (not A*):'
overall_A_level_and_FM = overall_available_combos_and_totals\
(A_level_best_grade_combos_and_totals, FM_best_grade_combos_and_totals)
#reduce FM best grade while optimizing Alevel best grade if the are no valid combos\
#for original (best individually) best grades for both A-level and FM
#store original (best individually) best grades for both A-level and FM as orginial_A_level_best_grade and\
#original_FM_best_grade
orginial_A_level_best_grade = A_level_best_grade
original_FM_best_grade = FM_best_grade
while overall_A_level_and_FM == []:
  # print to show user grades have been reduced  
  print('Reducing best grade as no available overall combos satisfying current best grades exist')
  FM_best_grade = reduce_best_grade(FM_best_grade)
  #if FM_best_grade is reducd to F (fail) then reduce A_level_best_grade and reset FM_best_grade to original 
  if FM_best_grade == 'F':
    A_level_best_grade = reduce_best_grade(A_level_best_grade)
    FM_best_grade = original_FM_best_grade
  #of A_level_best_grade is reduced to fail then inform user that no passing combination is available for award of A-level\
  #and FM. Reset A_level_best grade to original and output combo that optimizes for A-level in isolation
  if A_level_best_grade == 'F':
    print('No passing combination for A-level and FM possible :(')
    #output best grade and combo for A-level maths in isolation and end program
    A_level_best_grade = original_A_level_best_grade
    if bool_A_level_A_star(completed_module_results, A_level_best_grade):
      print('A-level: A*')
    else:
      print('A-level: {}'.format(A_level_best_grade))
    print('Overall combo with max sum of overall A-level and overall FM total:')
    print(A_level_only_max_combo)
    sys.exit()
  
  #recalculate A-level, FM and overall available combos and totals for reduced best grades
  A_level_best_grade_combos_and_totals = filter_above_total\
(A_level_available_combos_and_totals, grade_boundaries_dict[A_level_best_grade])
  FM_best_grade_combos_and_totals = filter_above_total(FM_available_combos_and_totals, grade_boundaries_dict[FM_best_grade])
  overall_A_level_and_FM = overall_available_combos_and_totals\
(A_level_best_grade_combos_and_totals, FM_best_grade_combos_and_totals)

#output to user the best available grades for A-level and FM in combination and the available combination that satisfies\
#these grades with the max sum of overall A-level and overall FM UMS   
if bool_A_level_A_star(completed_module_results, A_level_best_grade):
  print('A-level: A*')
else:
  print('A-level: {}'.format(A_level_best_grade))
print('FM: {}'.format(FM_best_grade)
max_combo = max_available_overall_combo(overall_A_level_and_FM)      
print('Overall combo with max sum of overall A-level and overall FM total:')
print(max_combo)  
  
  
 





