import itertools


# function to create space of overall A-Level valid module combinations
def overall_combos_A_level_space(compulsory_list, optional_combo_list):
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
    overall_combo_list.append(compulsory_combo_list[0] + list(optional_combo))

  for option_combo in FM_optional_combos_no_FP3:
    overall_combo_list.append(compulsory_combo_list[1] + list(optional_combo))
  
  return overall_combo_list

#function to create space of all possible 3 element combinations from IA2_FM_units_list 
def IA2_FM_units_combos_space(units_list):
  return list(itertools.combinations(units_list, 3))

#boolean function to check if valid combination is available for A-level requirements
#compulsory parameter stores A_level_compulsory_units list
#optional parameter stores A_level_optional_valid_combos list of combos
def A_level_module_requirements_check(completed, compulsory, optional):
  if len(completed) >= 6:
    completed_module_names = list(completed.keys())
    if all(list(map(lambda x: x in completed_module_names, compulsory)))\
& any([(combo[0] in completed_module_names) & (combo[1] in\
completed_module_names) for combo in optional]):
       return True
  return False
       
#boolean function to check if valid combination is available for FM requirements
#compulsory parameter stores FM_compulsory_valid_combos list of combos
def FM_module_requirements_check(completed, compulsory):
  if len(completed) >= 12:
    completed_module_names = list(completed.keys())
    if any([(combo[0] in completed_module_names) & (combo[1] in completed_module_names) for combo in compulsory]):
      return True
  return False

#function to return available valid 6 module combos from space of combination (A-Level or FM) or 3 module combos for IA2 FM units
#with total scores as ordered (descending by total UMS) list of tuples
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


#function to return only valid combos (ordered) with total above a minimum (int) from available_combos (list of tuples of combo tuples with totals) 
def filter_above_total(available_combos, minimum):
  filtered_list = list(filter(lambda x : x[1] >= minimum, available_combos))
  return sorted(filtered_list, key=lambda x:x[1], reverse=True)

#boolean function to determine if A_star at A-level is awarded
#max_A_level_grade parameter stores return value of max_grade_A_to_E \
#with first positional arg of A_level_available_combos_and_totals
def bool_A_level_A_star(completed, max_A_level_grade):
  if max_A_level_grade == 'A':
    sum_P3_P4 = completed['P3'] + completed['P4']
    if sum_P3_P4 >= 180:
      return True
  return False
  
#boolean function to determine if A_star at FM is possible for any available valid combo of FM modules
#IA2_available_A_star_combos stores return value of filter_above_total with argument of available valid IA2 FM unit combos
#max_grade_FM parameter stores return value of max_grade_A_to_E with argument of available FM combos
def bool_FM_A_star(IA2_available_A_star_combos, max_grade_FM):
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

#function to reduce the best possible grade by one grade
def reduce_best_grade(grade):
  return chr(ord(grade) + 1)

#function to display recommendation to user
def display_modules(max_tuple):
  if len(max_tuple[0]) >= 12:
    print('Optimized for max sum of overall A-level total and overall FM total')
    print('A-level modules: {}'.format(max_tuple[0][:6]))
    print('A-level total: {}'.format(max_tuple[1]))
    print('FM modules: {}'.format(max_tuple[0][6:]))
    print('FM total: {}'.format(max_tuple[2]))
  else:
    print('Optimized for max overall A-level total')
    print('A-level modules: {}'.format(max_tuple[0][:6]))
    print('A-level total: {}'.format(max_tuple[1]))
    

  