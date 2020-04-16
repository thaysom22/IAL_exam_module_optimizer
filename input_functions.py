#function to input modules and results and return as dict
def input_module_results(all_units):
  completed_module_results = {}
  print('Enter unit name and UMS score for each unit.\nWhen all results entered enter: \'done\'\n')
  
  temp_unit_title = input('Enter unit title: ').upper()
  while temp_unit_title != 'DONE':
    if temp_unit_title not in all_units:
      print('Enter valid unit title')
    else:
      temp_unit_result = input('Enter {} UMS score: '.format(temp_unit_title))
      
      while int(temp_unit_result) > 100 | int(temp_unit_result) < 0:
        temp_unit_result = input('Enter an integer between 0 and 100: ') 
      completed_module_results[temp_unit_title] = int(temp_unit_result)
    
    temp_unit_title = input('Enter unit title: ').upper()
   
  return completed_module_results
