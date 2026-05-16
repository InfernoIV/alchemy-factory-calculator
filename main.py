#imports
import sys
from commands import * #test, list, get, usage, dictionary, scale, calculate



#main function
def main():
    #handle the program
    error = handle_program(sys.argv)
    #if there is an error
    if error != None:
        #print the error
        print(f"Error: {error}, args: '{sys.argv}'")
        #print usage
        print_usage()



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
        #default to 0
        amount = 0
    #check all commands
    for command_entry in commands.keys():
        #if (fuzzy) match
        if command in command_entry:
            #run that command
            return commands[command_entry](resource, amount)
    #print error
    return f"command not found! {command}, {resource}, {amount}"
    


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
    #print commands
    print(f"Available commands: {', '.join(commands.keys())}")
    #exit
    sys.exit(1)



#exectue main function
main()


