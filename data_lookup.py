#script functions that handles the data from the CSV file into usable functionalities

#imports
import csv
from objects import recipe
from constants import ___CSV_RECIPES____, ___CSV_CAULDRON____

def get_recipes(resource):
    #get the recipe(s)
    return lookup_recipe(resource, ___CSV_RECIPES____)
    
def get_recipes_cauldron(resource):
    #get the recipe(s)
    return lookup_recipe(resource, ___CSV_CAULDRON____)


def lookup_recipe(resource, filename):
    #list to hold the matching recipes
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
                    recipe_object = recipe(row)
                    #add object to the list
                    matching_recipes.append(recipe_object)    

        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)

    #return the list of matching recipes
    return matching_recipes, None 
    