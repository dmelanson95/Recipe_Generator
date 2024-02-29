
import pandas as pd
from re import *


#takes inputWord as a string and returns the plural version of that word
def pluralize(inputWord: str) -> str:
    # checking whether the input word is ending with s,x,z or is
    # ending with ah, eh, ih, oh, uh, dh, gh, kh, ph, rh, th
    # with the regex pattern
    if search('[sxz]$', inputWord) or search('[^aeioudgkprt]h$', inputWord):
    # If it is true, then get the pluraof the inputWord by adding "es" in end
        return sub('$', 'es', inputWord)
    # checking whether the input word is ending with ay,ey,iy,oy,uy
    # with the other regex pattern
    elif search('[aeiou]y$', inputWord):
    # If it is true, then get the plural
    # of the word by removing 'y' from the end and adding ies to end
         return sub('y$', 'ies', inputWord)
    # Else add it just "s" to the word at the end to make it plural
    else:
        return inputWord + 's'

dnc_chars = ['(', ')', ',', '.', '["', '"]', ]

quantity_reg = compile(r"[\d\s\/]+")


#location folder name of file containing csv dataset
folder = 'C:/Users/dpfab/Desktop/Senior Design Project/'
#file name in folder
ds_dest = 'recipes_dataset.csv'
#read in 10 recipes at a time from csv file designated by folder string + ds_dest string
recipes = pd.read_csv(folder+ds_dest, chunksize = 1, iterator = False)

measurements = ['c.', 'tsp.', 'tbsp.', 'carton', 'can', 'box', 'g.', 'gallon', 'gal.']

ingredients = [i.lower() for i in list(pd.read_csv(folder+'ingredients_dataset.csv')['Aliased Ingredient Name'])]
ingredients.append('rice biscuit')
ingredients.append('brown sugar')
ingredients.append('sour cream')
ingredients.append('chicken breast')
ingredients.append('cream of mushroom')
ingredients.append('evaporated milk')
ingredients.append('chipped beef')


#loop to continue reading a chunk of recipes at a time
flag = True
while(flag):
    curr = next(recipes)

    ##############################################################################################
    ###############            Work with ingredients portion of dataset            ###############
    ##############################################################################################


    #call for next chunk of recipes and access only ingredients category in the same way dictionaries are accessed
    for i in curr['ingredients']:
        #replace nonsense characters with empty string
        curr_ing = i.replace('["', '').replace('"]', '').lower().split('", "')

        for i in measurements:
            if i in curr_ing:
                curr_meas = i
                curr_ing = curr_ing.replace(i, '')
        
        for ingredient_string in curr_ing:
            #print(ingredient_string)
            #list of potential ingredients found in string
            pot_ingredients = []
            for ingredient in ingredients:
                if ingredient in ingredient_string:
                    pot_ingredients.append(ingredient)
                    
            
            #get longest ingredient from list of potential ingredients
            #longest ingredient name should theoretically be the correct one
            curr_ingredient = max(pot_ingredients)
            plur_ing = pluralize(curr_ingredient)

            if plur_ing in ingredient_string:
                ingredient_string = ingredient_string.replace(plur_ing, '')
            else:
                ingredient_string = ingredient_string.replace(curr_ingredient, '')

            print(f'ingredient = {curr_ingredient}')

            quantity = quantity_reg.match(ingredient_string)
            print(f'quantity = {quantity.group(0)}')

            ingredient_string = ingredient_string.replace(quantity.group(0), '')
            pot_m = []
            for measurement in measurements:
                if measurement in ingredient_string:
                    pot_m.append(measurement)

            measurement = max(pot_m) if pot_m else ""
            ingredient_string = ingredient_string.replace(measurement, '')

            print(f'measurement = {measurement}')
    
    ##############################################################################################
    ###############             Work with directions portion of dataset            ###############
    ##############################################################################################
            
    for i in curr['directions']:
        curr_dir = i.replace('["', '').replace('"]', '').lower().split('", "')

        for instruction in curr_dir:
            #fix degree sign in directions
            instruction = instruction.replace('\\u00b0',u'\N{DEGREE SIGN}')
            
            print(instruction)
            



    #take user input and continue if Y    
    temp = input('Continue?\tY/N\n')
    if temp.upper() == 'N':
        flag = False


