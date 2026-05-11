#script functions that handles the data from the CSV file into usable functionalities

#imports
import csv
from objects import recipe
from constants import ___CSV_RECIPES____, ___CSV_CAULDRON____, ___PREFERRED_RECIPES___


#main function
#returns recipe, by-products, error
def get_recipe(resource):
    #always prioritize cauldron recipe first (it's there for a reason...)
    cauldron_recipe, error = get_recipe_cauldron(resource)
    #if error
    if error != None:
        #return error
        return None, None, error
    
    #if there is a cauldron recipe
    elif cauldron_recipe != None:
        #return the cauldron recipe
        return cauldron_recipe, None, None
    
    #otherwise
    else:
        #get normal recipes
        recipes, error = get_recipes(resource)
        
        #if error
        if error != None:
            #return error
            return None, None, error
        
        #if no recipes found
        if len(recipes) == 0:
            #return nothing
            return None, None, None
        
        else:
            #set chosen recipe
            chosen_recipe = None

            #only 1 index
            if len(recipes) == 1:
                #take the first index
                chosen_recipe = recipes[0]

                
            #if multiple recipe's found
            else:
                #for each recipe
                for recipe in recipes:
                    #if it is a preferred recipe
                    if recipe.name in ___PREFERRED_RECIPES___:
                        #return this recipe
                        chosen_recipe = recipe
                        
                        break
                #return None, None, "Multiple recipes, but no preferred recipe!"
            
            #get all output of this recipe
            all_output_of_recipe, error = get_recipes_by_name(chosen_recipe.name, resource)

            #check for errors
            if error != None:
                return None, None, error
            
            return chosen_recipe, all_output_of_recipe, None
            


#lookup recipe by name (to determine by-products)
def get_recipes_by_name(name, resource):
    filename = ___CSV_RECIPES____
    #list of recipes
    matching_recipes = []
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #if found, but not the resource we are looking for = by-product
                if name.lower() == row["recipe-name"].lower() and resource.lower() != row["output-resource"].lower():
                    #create recipe object
                    recipe_object = recipe(row, False, True)
                    #add object to the list
                    matching_recipes.append(recipe_object)    

        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)

    #return the list of matching recipes
    return matching_recipes, None 



#get recipes for a resource
def get_recipes(resource):
    filename = ___CSV_RECIPES____
    #list of recipes
    matching_recipes = []

    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #if found
                if resource.lower() == row["output-resource"].lower():
                    #create recipe object
                    recipe_object = recipe(row, False)
                    #add object to the list
                    matching_recipes.append(recipe_object)    

        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)

    #return the list of matching recipes
    return matching_recipes, None 
    


#get cauldron recipe for resource
def get_recipe_cauldron(resource):
    #set filename
    filename = ___CSV_CAULDRON____
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #if found
                if resource.lower() == row["output-resource"].lower():
                    #create recipe object, indicating it is 
                    recipe_object = recipe(row, True)
                    return recipe_object, None

        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)

    #return the list of matching recipes
    return None, None 
    
    
