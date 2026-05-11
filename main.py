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
    #remove the script name, only keeping arguments
    arguments.pop(0)
    #save the number of arguments for easy lookup
    number_of_arguments = len(arguments)
    #check if there are arguments
    if number_of_arguments < 1:
        #set error
        return None, None, SyntaxError("No arguments!")
    
    #there are arguments
    else:
        #if the last argument is a digit
        if arguments[number_of_arguments-1].isdigit():
            #this should be amount
            amount = int(arguments[number_of_arguments-1])
            #the rest are text for the resource
            resource = " ".join(arguments[:number_of_arguments-1]).lower()
            #return data
            return resource, amount, None
        
        #only text
        else:
            #all text for resource
            resource = " ".join(arguments).lower()
            #return data
            return resource, None, None



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
        pass
    


def collect_recipe(recipe_list, resource, amount):
    #lookup recipe
    recipe, by_products, error = get_recipe(resource)
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

        #handle by_products
        if by_products != None:
            for by_product in by_products:
                #remove the inputs (it's a by product)
                by_product.inputs = {}
                #add to list
                recipe_list.append(by_product)


        #for every input
        for inner_resouce, inner_amount in recipe.inputs.items():
            #collect the recipe
            collect_recipe(recipe_list, inner_resouce, inner_amount) 



def print_table():
    pass

#exectue main function
main()