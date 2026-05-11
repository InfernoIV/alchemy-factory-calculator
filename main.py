#imports
import sys
from objects import recipe
from data_lookup import get_recipe

#main function
def main():
    #handle the program
    error = handle_program(sys.argv)
    #if there is an error
    if error != None:
        #print the error
        print(f"Error: {error}")
        #print usage
        print_usage()
    #stop function
    return



#function that handles the program, returns if there is an error
def handle_program(arguments): 
    #check and convert the input
    resource, amount, error = process_input(arguments)
    if error != None:
        return error

    #debug
    #print("Input: ", amount, " * ", resource)
    #calculate resources
    calculate_resource(resource, amount)

    return None

    #not a valid command
    return SyntaxError("No resource found!")



#function that checks the input arguments
def process_input(arguments):    
    #check if there are arguments
    if len(arguments) < 2:
        #set error
        return None, None, SyntaxError("No arguments!")
    elif len(arguments) > 3:
        #set error
        return None, None, SyntaxError("Too many arguments!")
    else:
        #correct amount of arguments, check arguments
        if sys.argv[1].isdigit():
            #set error
            return None, None, SyntaxError("Resource is a number!")
        
        #get the resource
        resource = sys.argv[1].lower()
        
        #if no amount provided
        if len(arguments) == 2:
            #just return the resource
            return resource, None, None
        else:
            #get the amount
            amount = int(sys.argv[2])
            #return all
            return resource, amount, None



#prints the usage of the program
def print_usage():
    #print help message
    print("Usage: python3 main.py \"<resource>\" <amount>")
    #exit
    sys.exit(1)
    #needed?
    return



def calculate_resource(resource, amount):
    recipe_list = []
    collect_recipe(recipe_list, resource, amount)
    for recipe in recipe_list:
        print(recipe)
    


def collect_recipe(recipe_list, resource, amount):
    #lookup recipe
    recipe, error = get_recipe(resource)
    #check for error
    if error != None:
        #return error
        return None, error
    #recipe is available
    if recipe != None:
        #check if amount needs to be changed
        if amount != None:
            #change amount
            recipe.adjust_amount(amount)

        #add recipe to the list
        recipe_list.append(recipe)

        #for every input
        for inner_resouce, inner_amount in recipe.inputs.items():
            #collect the recipe
            collect_recipe(recipe_list, inner_resouce, inner_amount) 



def print_table():
    pass

#exectue main function
main()