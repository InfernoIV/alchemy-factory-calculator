#imports
import sys
from objects import recipe
from data_lookup import get_recipes, get_recipes_cauldron

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
    print("Input: ", amount, " * ", resource)
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
        if not sys.argv[2].isdigit():
            #set error
            return None, None, SyntaxError("Amount is not a number!")
        
        #get the resource
        resource = sys.argv[1].lower()
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
    recipes = get_recipes(resource)
    print("recipes: ", recipes)
    return None



#exectue main function
main()