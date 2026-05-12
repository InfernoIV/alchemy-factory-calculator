#imports
import sys
from recipe import get_recipe, get_recipe_list



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
    command, resource, amount, error = process_input(arguments)
    #if an error has occurred
    if error != None:
        #return the error
        return error
    #if no amount specified
    if amount == None:
        #default to 1
        amount = 1

   

    #calculate resources
    #calculate_resource(resource, amount)
    if command in "test":
        #print(f"command: {command}, resource: {resource}, amount: {amount}")
        recipe, error = get_recipe("steel ingot")
        #check for error
        if error != None: return error            
        #print
        print(f"recipe: {recipe}")

    elif command in "get":
        #get the recipe
        recipe, error = get_recipe(resource)
        #check for error
        if error != None: return error
        #print
        print(recipe)

    elif command in "list":
        recipe_list = get_recipe_list(resource)
        #print
        for recipe in recipe_list:
            print(recipe.description_fast())

    elif command in "scale" or command in "calculate":
    #   calculate_recipe(resource,amount)
        pass

    #indicate no error
    return None



#function that checks the input arguments
def process_input(arguments):  
    #remove the script name, only keeping arguments
    arguments.pop(0)
    #save the number of arguments for easy lookup
    number_of_arguments = len(arguments)
    #check if there are arguments
    if number_of_arguments < 2:
        #set error
        return None, None, None, SyntaxError("Not enough arguments!")
    #there are arguments
    else:
        #get the command
        command = arguments[0]
        #if the last argument is a digit
        if arguments[number_of_arguments-1].isdigit():
            #this should be amount
            amount = int(arguments[number_of_arguments-1])
            #the rest are text for the resource
            resource = " ".join(arguments[1:number_of_arguments-1]).lower()
            #return data
            return command, resource, amount, None
        #only text
        else:
            #all text for resource
            resource = " ".join(arguments[1:]).lower()
            #return data
            return command, resource, None, None



#prints the usage of the program
def print_usage():
    #print help message
    print("Usage: python3 main.py <command> <resource>")
    #print help message (alt usage)
    print("Usage: python3 main.py <command> <resource> <amount>")
    #exit
    sys.exit(1)



#exectue main function
main()