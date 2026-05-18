from recipe import *
from cauldron import *



def test(resource, amount):
    #print(f"test function: {command}, {resource}, {amount}")
    #print(f"command: {command}, resource: {resource}, amount: {amount}")
    recipe, error = get_recipe("steel ingot")
    #check for error
    if error != None: return error            
    #print
    print(f"recipe: {recipe}")



def get(resource, amount):
    #get the recipe
    recipe, error = get_recipe(resource)
    #check for error
    if error != None: return error
    #print
    print(recipe)



def list(resource, amount):
    #get list of all recipes needed for this resource
        recipe_list = get_recipe_list(resource)
        #for each recipe
        for recipe in recipe_list:
            #print
            print(recipe.description_fast())



def dictionary(resource, amount):
    #get dict of all recipes needed for this resource
    recipe_dict, error = get_recipe_dict(resource)
    #check for error
    if error != None:
        #return the error
        return error
    #for each recipe
    for name, recipe in recipe_dict.items():
        #print
        print(recipe.description_fast())



def scale(resource, amount):
    #scale recipe
    recipe, error = scale_recipe(resource, amount)
    #check for error
    if error != None:
        #return the error
        return error
    #if we have a recipe
    if recipe != None:
        #print
        print(recipe.description_fast())
    #if there is no recipe
    else:
        #debug
        print(f"No recipe found for '{amount}' '{resource}'")



def calculate(resource, amount):
        #if no amount set
        if amount == 0:
            #get the base recipe set
            recipe, error = get_recipe(resource)
            #check for errors
            if error != None:
                #return
                return error
            if recipe == None:
                #return message
                return f"No recipe found for '{resource}'"
            #set the amount
            amount = recipe.outputs[resource]
        #get the list of tuples of amount and recipes
        calculated_dict, resource_extra, by_products, error = calculate_recipe(resource,amount)
        #check for error
        if error != None:
            #return the error
            return error
        #start message
        print(f"{amount} {resource} requires: ")
        #for each recipe
        for recipe_name, recipe in calculated_dict.items():
            #create a spacer according to the depth
            spacer = "--" * recipe.depth
            #print
            print(f"{spacer} {recipe.description_fast()}") #{recipe.device_amount} {recipe.device} with recipe '{recipe_name}' to create {recipe.outputs}")
        print("")
        print(f"by-products: {by_products}")    
        
           

def usage(resource, amount):
        #get the usage of a resource
        recipes, error = get_usage(resource)
        #check error
        if error != None:
            #return error
            return error
        if len(recipes) > 0:
            #start print
            print(f"possible usage of '{resource}':")
            #for every recipe
            for recipe_name, recipe in recipes.items():
                #print the recipes
                print(recipe.description_fast())
        else:
            #start print
            print(f"No possible usage of '{resource}'!")



def cauldron(resource, amount):
    #calucate the cauldron recipes for the resource
    calculate_cauldron(resource, 2)



#at the bottom due to function declarations
#define the commands to be used (for easy readability)
commands = {
    "test":test,
    "list":list,
    "get":get,
    "dictionary":dictionary,
    "scale":scale,
    "calculate":calculate,
    "usage":usage,
    "cauldron":cauldron,
}