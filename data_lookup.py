#script functions that handles the data from the CSV file into usable functionalities

#imports
import csv
from objects import recipe
from constants import ___CSV_RECIPES____, ___CSV_CAULDRON____

def get_recipe(resource):
    #always prioritize cauldron recipe first (it's there for a reason...)
    cauldron_recipe, error = get_recipe_cauldron(resource)
    #if error
    if error != None:
        #return error
        return None, error
    #if there is a cauldron recipe
    elif cauldron_recipe != None:
        #return the cauldron recipe
        return cauldron_recipe, None
    #otherwise
    else:
        #get normal recipes
        recipes, error = get_recipes(resource)
         #if error
        if error != None:
            #return error
            return None, error
        if len(recipes) == 0:
            return None, None
        else:
            #TODO: recipe selection / prioritization
            #return the first recipe for now
            return recipes[0], None



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
    
    
