import random

from functions import overall_combos_FM

#container variables declared in optimize.py script.
all_units = ['P1', 'P2', 'P3', 'P4', 'FP1', 'FP2', 'FP3', 'M1', 'M2', 'M3', 'S1', 'S2', 'S3', 'D1']
IAS_units = ['P1', 'P2', 'FP1', 'M1', 'S1', 'D1']
IA2_FM_units_list = ['FP2', 'FP3', 'M2', 'M3', 'S2', 'S3']
A_level_compulsory_units = ['P1', 'P2', 'P3', 'P4']
A_level_optional_units = ['D1', 'M1', 'S1', 'M2', 'S2']
A_level_optional_valid_combos = [['M1', 'M2'], ['S1', 'S2'], ['M1', 'S1'], ['D1', 'S1'], ['D1', 'M1']]
FM_compulsory_combos = [['FP1', 'FP2'], ['FP1', 'FP3']] 
FM_optional_units = ['FP2', 'FP3', 'M1', 'M2', 'M3', 'S1', 'S2', 'S3', 'D1']
FM_optional_valid_combos = [['FP1', 'FP2'], ['FP1', 'FP3']]
grade_boundaries_dict = {'A':480, 'B':420, 'C':360, 'D':300, 'E':240}

# function to generate a 12 random module dict of random module results that satisfies valid combos for A-level and for FM
def generate_random_module_results(A_level_compulsory_units, A_level_optional_valid_combos, FM_compulsory_combos, FM_optional_units):
  module_results = {}
  
  for unit in A_level_compulsory_units:
    module_results[unit] = random.randint(40, 100)
  
  A_level_option_combo = random.choice(A_level_optional_valid_combos):
  for unit in A_level_option_combo:   
    module_results[unit] = random.randint(40, 100)
    FM_optional_units.remove(unit)
  FM_optional_units_reduced = FM_optional_units
  
  FM_possible_combos_space = overall_combos_FM_space(FM_compulsory_combos, FM_optional_units_reduced)
  random_FM_combo = random.choice(FM_possible_combos_space)
  for unit in random_FM_combo:
    module_results[unit] = random.randint(40, 100)
    
  return module_results
    
    
  
   
