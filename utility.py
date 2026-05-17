import inspect, sys

def final_print(*variables):
    frame = inspect.currentframe().f_back
    print(frame.f_locals.items())
    #print(f"variables: '{variables}'")

#stepping stone
def print_variables(*variables):
    #pass it along, to filter only specific variables
    #final_print(variables)
    #return
    #initialize the string
    string = ""
    #for each variable
    #for name, value in variables:
    for value in variables:
        #if string has data
        if string != "":
            #add a comma
            string += ", "
        #add the data
        #string += f"{name}: '{value}'"
        string += f"'{value}'"
    #print the string
    #print(string)
    #sys.exit()

