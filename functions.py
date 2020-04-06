import itertools
import random

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
def overall_combos_FM(compulsory_combo_list, optional_list):
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

#function to create list of 3 element combinations from IA2_FM_units_list 
def IA2_FM_units_combos(units_list):
  return list(itertools.combinations(units_list, 3))


# function to store inputted module results as dict
def input_modules_results(all_units):
  completed_module_results = {}
  print('Enter UMS score for each unit.\nIf no result recorded for this unit enter: \'n\'\nWhen all results entered enter: \'d\'\n')

  for unit in all_units:
    unit_result = input('Enter {} UMS: '.format(unit))
    if unit_result.lower() == 'd':
      break
    elif unit_result.lower() == 'n' or unit_result.lower() == '':
      continue
    else:
      completed_module_results[unit] = int(unit_result)
  return completed_module_results

# function to return possible valid A-Level or FM combos with total scores as ordered list of tuples
def valid_combos_ordered(completed, poss_combos):
  list_combo_totals = []
  for combo in poss_combos:
    if set(combo).issubset(set(list(completed.keys()))):
      combo_results = list(map(lambda module: completed[module], combo))
      list_combo_totals.append((tuple(combo), sum(combo_results)))
  if list_combo_totals is not []:
    return sorted(list_combo_totals, key=lambda x:x[1], reverse=True)
  else:
    return None

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


   



