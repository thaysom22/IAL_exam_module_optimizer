###TODO###
#Store container variables in separate file and import to this module
#Add function to optimization_functions to perform A* check for A-level
#Complete README file

import sys

from optimization_functions import *

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



# create spaces of valid combos for A-level, FM and FM IA2 units by calling functions invoking itertools
A_level_combos_space = overall_combos_A_level_space(A_level_compulsory_units, A_level_optional_valid_combos)
FM_combos_space = overall_combos_FM_space(FM_compulsory_valid_combos, FM_optional_units)
IA2_FM_combos_space = IA2_FM_units_combos_space(IA2_FM_units_list)

###BOOKMARK###

#generate/input module results
completed_module_results = generate_random_module_results(all_units)

#calculate totals for possible combos and order 
A_level_valid_combos_and_totals = valid_combos_ordered(completed_module_results, A_level_overall_combos)
FM_valid_combos_and_totals = valid_combos_ordered(completed_module_results, FM_overall_combos)
IA2_units_valid_combos_and_totals = valid_combos_ordered(completed_module_results, IA2_units_overall_combos)

#calculate max possible grade A to E at A-level and at FM
A_level_best_grade = max_grade_A_to_E(A_level_valid_combos_and_totals, grade_boundaries_dict)
if not A_level_best_grade:
  sys.exit()

FM_best_grade = max_grade_A_to_E(FM_valid_combos_and_totals, grade_boundaries_dict)

#filter A_level_valid_combos_and_totals and FM_valid_combos_and_totals for combos with total satisfying max grade requirement
grade_A_level_valid_combos_and_totals = filter_above_total(A_level_valid_combos_and_totals, grade_boundaries_dict[A_level_best_grade])
grade_FM_valid_combos_and_totals =filter_above_total(FM_valid_combos_and_totals, grade_boundaries_dict[FM_best_grade])


#filter IA2_units_valid_combos_and_totals for A* combos
IA2_units_valid_A_star_combos = filter_above_total(IA2_units_valid_combos_and_totals, 270)

#create list of tuples of overall FM combos that satify A* requirements
overall_FM_A_star_combos = valid_overall_A_star_FM_combos(grade_FM_valid_combos_and_totals, IA2_units_valid_A_star_combos)

#bool for A* at FM possible
bool_FM_A_star = bool_FM_A_star_possible(IA2_units_valid_A_star_combos, FM_best_grade)



#print tests
print('Completed module results as dict:')
print(completed_module_results)
print()
#print('Ordered list of valid A-level module combos as tuples with totals:')
#print(A_level_valid_combos_and_totals)
#print()
#print('Ordered list of valid FM module combos as tuples with totals:')
#print(FM_valid_combos_and_totals)
#print()

#print('Ordered list of valid A-level module combos satisfying max grade requirement as tuples with totals:')
#print(grade_A_level_valid_combos_and_totals)
#print()

#print('Ordered list of valid FM module combos satisfying max grade requirement as tuples with totals:')
#print(grade_FM_valid_combos_and_totals)
#print()


print('A* at FM possible?')
print(bool_FM_A_star)
print()

#test
print('Best grades possible individually:')
print('Best grade A to E at A-level possible:')
print(A_level_best_grade)
print()
print('Best grade A to E at FM possible:')
print(FM_best_grade)
print()

#split flow by if A* at FM is possible
check = 0
if bool_FM_A_star:
  #print('Ordered list of valid IA2 module combos as tuples with totals:')
  #print(IA2_units_valid_combos_and_totals)
  #print()
  print('Ordered list of valid IA2 module A* combos as tuples with totals:')
  print(IA2_units_valid_A_star_combos)
  print()
  print('List of tuples of overall FM combos that satify A* requirements:')
  print(overall_FM_A_star_combos)
  print()
  
  overall_A_level_and_FM_A_star = overall_combos_and_totals(grade_A_level_valid_combos_and_totals, overall_FM_A_star_combos)
  if overall_A_level_and_FM_A_star == []:
    check = 1
  else:

    print('List of overall module combos and totals that satisfy max possible grade requirements for A level and A* for FM:')
    print(overall_A_level_and_FM_A_star)
    print()

    max_combo = max_overall_combo(overall_A_level_and_FM_A_star)
    print('Overall combo with max sum of overall A-level and overall FM total:')
    print(max_combo)
    print()
    check = 2  
    



if check == 0 or check == 1:
  
  #create list of overall module combos and totals that satisfy max possible grade requirements for A level and for FM:'
  overall_A_level_and_FM = overall_combos_and_totals(grade_A_level_valid_combos_and_totals, grade_FM_valid_combos_and_totals)

  #reduce FM best grade while optimizing Alevel best grade if the are no valid combos for original max gradesfor both A-level and FM
  orginial_A_level_best_grade = A_level_best_grade
  original_FM_best_grade = FM_best_grade
  while overall_A_level_and_FM == []:
    print('Reducing best grade as no valid overall combos exist')
    FM_best_grade = chr(ord(FM_best_grade) + 1)
    if FM_best_grade == 'F':
      A_level_best_grade = chr(ord(A_level_best_grade) + 1)
      FM_best_grade = original_FM_best_grade
    if A_level_best_grade == 'F':
      print('No passing combination possible :(')
      break
    grade_A_level_valid_combos_and_totals = filter_above_total(A_level_valid_combos_and_totals, grade_boundaries_dict[A_level_best_grade])
    grade_FM_valid_combos_and_totals = filter_above_total(FM_valid_combos_and_totals, grade_boundaries_dict[FM_best_grade])
    overall_A_level_and_FM = overall_combos_and_totals(grade_A_level_valid_combos_and_totals, grade_FM_valid_combos_and_totals)

  print()
  print('Best grades possible in overall combination:')
  print('Best grade A to E at A-level possible:')
  print(A_level_best_grade)
  print()
  print('Best grade A to E at FM possible:')
  print(FM_best_grade)
  print()
  print('List of overall module combos and totals that satisfy max possible grade requirements for A level and for FM:')

  print(overall_A_level_and_FM)
  print()
  #max tuple from overall_combos_and_totals overall A-level and overall FM total by sum of A level and FM totals
  max_combo = max_overall_combo(overall_A_level_and_FM)
  print('Overall combo with max sum of overall A-level and overall FM total:')
  print(max_combo)
  print()
  



#TODO Add check for Alevel and FM module combination requirements met
#TODO add boolean function for A* at A-level possible (call once best grade in overall combination has been calculated) 
