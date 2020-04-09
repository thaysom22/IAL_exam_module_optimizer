import itertools

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

#function to create space of all possible 3 element combinations from IA2_FM_units_list 
def IA2_FM_units_combos_space(units_list):
  return list(itertools.combinations(units_list, 3))



#function to return available valid 6 module combos from space of combination (A-Level or FM) or 3 module combos for IA2 FM units
# with total scores as ordered (descending by total UMS) list of tuples
def available_combos_ordered(completed, combo_space):
  list_combo_totals = []
  for combo in combo_space:
    if set(combo).issubset(set(completed.keys())):
      combo_results = list(map(lambda module: completed[module], combo))
      list_combo_totals.append((tuple(combo), sum(combo_results)))
  if list_combo_totals:
    return sorted(list_combo_totals, key=lambda x:x[1], reverse=True)
  else:
    return False
 
#function to return max grade A to E possible for available combinations (A-level or FM)
#available_combos parameter stores return value of valid_combos_ordered function
def max_grade_A_to_E(available_combos, grade_boundaries):
  if available_combos:
    for grade in ['A', 'B', 'C', 'D', 'E']:
      if available_combos[0][1] >= grade_boundaries[grade]:
        return grade
    return False

#boolean function to check if valid combination is available and total UMS requirement met for any A-level pass (E or above)
#max_grade parameter stores return value of max_grade_A_to_E function
def A_level_pass_check(max_grade):
  if max_grade:
    return True
  return False

#boolean function to check if valid combination is available for FM requirements
#A_level pass parameter stores boolean return value if A_level_pass_check function
def FM_module_requirements_check(A_level_pass, completed):
  if A_level_pass & len(completed) >= 12 & \ 
(('FP1' in completed.keys() & 'FP2' in completed.keys()) | ('FP1' in completed.keys() & 'FP3' in completed.keys())):
    return True
  return False

#function to return only valid combos (ordered) with total above a minimum (int) from available_combos (list of tuples of combo tuples with totals) 
def filter_above_total(available_combos, minimum):
  filtered_list = list(filter(lambda x : x[1] >= minimum, available_combos))
  return sorted(filtered_list, key=lambda x:x[1], reverse=True)

#boolean function to determine if A_star at FM is possible for any available valid combo of FM modules
#IA2_available_A_star_combos stores return value of filter_above_total with argument of available valid IA2 FM unit combos
#max_grade_FM parameter stores return value of max_grade_A_to_E with argument of available FM combos
def bool_FM_A_star_possible(IA2_available_A_star_combos, max_grade_FM):
  if max_grade_FM == 'A':
    if IA2_available_A_star_combos:
      return True
  return False

#function to filter available overall FM combos that obtain A* grade and return as (ordered by total) list of tuples
#available_grade_A_FM_combos parameter stores available FM combos filtered to leave combos that obtain A grade total 
#IA2_available_A_star_combos stores return value of filter_above_total with argument of available valid IA2 FM unit combos
def available_overall_A_star_FM_combos(available_grade_A_FM_combos, IA2_available_A_star_combos):
  overall_list = []
  for combo in IA2_available_A_star_combos:
    filtered_list = list(filter(lambda x : set(combo[0]).issubset(set(x[0])), available_grade_A_FM_combos))
    overall_list.extend(filtered_list)
  return overall_list

#function to return available overall combos and totals while satisfying best grade possible at A level and FM if 
#bool_FM_A_star_possible is False
#A_level_combos parameter stores available A_level module combinations that satisfy the requirments to achieve the 
#best possible available grade
#FM_combos parameter stores available FM module combinations that satisfy the requirments to achieve the 
#best possible available grade
def overall_available_combos_and_totals(A_level_combos, FM_combos):
  overall_list = []
  for A_level_combo in A_level_combos:
    for FM_combo in FM_combos:
      #if both optional modules at A level are not in a FM available combo then append to list a tuple consisting
      #of the concatenation of the A level combo and the FM combo, the A level combo UMS total and the FM combo UMS total
      if ((A_level_combo[0][-2] not in FM_combo[0]) and (A_level_combo[0][-1] not in FM_combo[0])):
        overall_list.append((A_level_combo[0]+FM_combo[0], A_level_combo[1], FM_combo[1]))
  return overall_list

#function to return overall_combos_and_totals with the maximum sum of overall A-level and overall FM total 
#(returns False if list of available overall module combos and totals that satisfy max grade requirement 
#for A-level and FM is empty)
#list_of_available_overall_combos paraemter stores return value of overall_available_combos_and_totals function
def max_available_overall_combo(list_of_available_overall_combos):
  return list_of_available_overall_combos[0]


   



