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
    #if an error has occurred
    if error != None:
        #return the error
        return error
    #calculate resources
    calculate_resource(resource, amount)
    #indicate no error
    return None



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
    print("Usage: python3 main.py <resource>")
    #print help message (alt usage)
    print("Usage: python3 main.py <resource> <amount>")
    #exit
    sys.exit(1)



#calculate the needed resources
def calculate_resource(resource, amount):
    #list to fill with recipes
    recipe_list = []
    #collect all underlying recepies, calling itself multiple times to dig deeper
    collect_recipe(recipe_list, resource, amount)
    #print
    for depth, recipe in recipe_list:
        #add extra markings to indicate depth
        message = ("-" * 2 * depth)
        #if there is depth
        if depth > 0:
            #add a space
            message += " " 
        #add the description of the recipe
        message += recipe.get_small_description()
        #print the message
        print(message)
    


#gather all recipes from the original recipes, drilling down within every recipe
def collect_recipe(recipe_list, resource, amount, depth = 0):
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
        recipe_list.append((depth,recipe))
        #handle by_products
        if by_products != None:
            for by_product in by_products:
                #remove the inputs (it's a by product)
                by_product.inputs = {}
                #set the device amount the same as the original
                by_product.adjust_device_amount(recipe.device_amount)
                #add to list
                recipe_list.append((depth,by_product))
        #for every input
        for inner_resouce, inner_amount in recipe.inputs.items():
            #collect the recipe
            collect_recipe(recipe_list, inner_resouce, inner_amount, depth+1) 



#exectue main function
main()
