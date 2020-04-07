import itertools
import random

###TODO### 
#Create boolean output functions to determine if module combo requirements of A-Level/FM are met 

###
#container variables declared in optimize.py script. Commented here for reference. 
#all_units = ['P1', 'P2', 'P3', 'P4', 'FP1', 'FP2', 'FP3', 'M1', 'M2', 'M3', 'S1', 'S2', 'S3', 'D1']
#IAS_units = ['P1', 'P2', 'FP1', 'M1', 'S1', 'D1']
#IA2_FM_units_list = ['FP2', 'FP3', 'M2', 'M3', 'S2', 'S3']
#A_level_compulsory_units = ['P1', 'P2', 'P3', 'P4']
#A_level_optional_units = ['D1', 'M1', 'S1', 'M2', 'S2']
#A_level_optional_valid_combos = [['M1', 'M2'], ['S1', 'S2'], ['M1', 'S1'], ['D1', 'S1'], ['D1', 'M1']]
#FM_compulsory_combos = [['FP1', 'FP2'], ['FP1', 'FP3']] 
#FM_optional_units = ['FP2', 'FP3', 'M1', 'M2', 'M3', 'S1', 'S2', 'S3', 'D1']
#FM_optional_valid_combos = [['FP1', 'FP2'], ['FP1', 'FP3']]
#grade_boundaries_dict = {'A':480, 'B':420, 'C':360, 'D':300, 'E':240}
###

# function to create space of overall A-Level valid module combinations
def overall_combos_A_level(compulsory_list, optional_combo_list):
  overall_combo_list = []
  for optional_combo in optional_combo_list:
    overall_combo = compulsory_list + optional_combo
    overall_combo_list.append(overall_combo)
  return overall_combo_list

# function to create space of overall FM combination options
def overall_combos_FM_space(compulsory_combo_list, optional_list):
  overall_combo_list = []
  copy1 = optional_list.copy()
  copy2 = optional_list.copy()
  copy1.remove('FP2')
  FM_optional_list_no_FP2 = copy1
  FM_optional_combos_no_FP2 = list(itertools.combinations(FM_optional_list_no_FP2, 4))
  copy2.remove('FP3')
  FM_optional_list_no_FP3 = copy2
  FM_optional_combos_no_FP3 = list(itertools.combinations(FM_optional_list_no_FP3, 4))
 
  for optional_combo in FM_optional_combos_no_FP2:
    overall_combo_list.append(compulsory_combo_list[0] + option_combo)

  for option_combo in FM_optional_combos_no_FP3:
    overall_combo_list.append(compulsory_combo_list[1] + option_combo)
  
  return overall_combo_list

#function to create list of all possible 3 element combinations from IA2_FM_units_list 
def IA2_FM_units_combos(units_list):
  return list(itertools.combinations(units_list, 3))


#function to input modules and results and return as dict
def input_module_results(all_units):
  completed_module_results = {}
  print('Enter unit name and UMS score for each unit.\nWhen all results entered enter: \'done\'\n')
  
  temp_unit_title = input('Enter unit title: ').upper()
  while temp_unit_title != 'DONE':
    if temp_unit_title not in all_units.keys():
      print('Enter valid unit title')
    else:
      temp_unit_result = input('Enter {} UMS score: '.format(temp_unit_title))
      
      while int(temp_unit_result) > 100 | int(temp_unit_result) < 0:
        temp_unit_result = input('Enter an integer between 0 and 100: ') 
      completed_module_results[temp_unit_title] = int(temp_unit_result)
    
    temp_unit_title = input('Enter unit title: ').upper()
   
  return completed_module_results

#function to return available valid 6 module combos from space of combination (A-Level or FM) with total scores as ordered (descending by total UMS) list of tuples
def valid_combos_ordered(completed, combo_space):
  list_combo_totals = []
  for combo in combo_space:
    if set(combo).issubset(set(completed.keys())):
      combo_results = list(map(lambda module: completed[module], combo))
      list_combo_totals.append((tuple(combo), sum(combo_results)))
  if list_combo_totals:
    return sorted(list_combo_totals, key=lambda x:x[1], reverse=True)
  else:
    return False
  
#boolean function to check if valid combination and grade requirement met for A-level
#available_combos variable stores return value of valid_combos_ordered function
def A_level_pass_check(available_combos):
  if available_combos:
    if available_combos[0][1] >= grade_boundaries_dict['E']:
      return True
  return False  
 
###BOOKMARK###
# function to return max grade A to E possible (A-level or FM)
def max_grade_A_to_E(combos_with_totals, grade_boundaries):
  for grade in ['A', 'B', 'C', 'D', 'E']:
    if combos_with_totals[0][1] >= grade_boundaries[grade]:
      return grade
  return False

# function to return only valid combos (ordered) with total above minimum from list of tuples of combos with totals 
def filter_above_total(list_of_tuples, minimum):
  filtered_list = list(filter(lambda x : x[1] >= minimum, list_of_tuples))
  return sorted(filtered_list, key=lambda x:x[1], reverse=True)

# boolean function to determine if A_star at FM is possible
def bool_FM_A_star_possible(IA2_A_star_modules, A_requirement):
  if A_requirement == 'A':
    return IA2_A_star_modules != []
  else:
    return False

# function to filter valid overall FM combos that obtain A* grade and return ordered list
def valid_overall_A_star_FM_combos(combos_and_totals, A_star_combos):
  overall_list = []
  for combo in A_star_combos:
    filtered_list = list(filter(lambda x : set(combo[0]).issubset(set(x[0])), combos_and_totals))
    overall_list.extend(filtered_list)
  return overall_list

# function to return valid overall combos and totals while satisfying best grade possible at A level and FM if bool_FM_A_star_possible is False
def overall_combos_and_totals(A_level_combos, FM_combos):
  overall_list = []
  for A_level_combo in A_level_combos:
    for FM_combo in FM_combos:
      if ((A_level_combo[0][-2] not in FM_combo[0]) and (A_level_combo[0][-1] not in FM_combo[0])):
        overall_list.append((A_level_combo[0]+FM_combo[0], A_level_combo[1], FM_combo[1]))
  return overall_list

# function to return overall_combos_and_totals max sum of overall A-level and overall FM total (if list of overall module combos and totals that satisfy max grade requirement for A-level and FM is not empty)
def max_overall_combo(overall_list_of_tuples):
  return overall_list_of_tuples[0]


   



