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



#function to format a number with a precision
def format_precision(number, max_precision = 2):
    #for 0 to max precision
    for i in range(max_precision+1):
        #check if this precision does not results into a 0 (which means the precision is correct)
        if float(f"{number:.{i}f}") != 0:
                #return this precision string
                return f"{number:.{i}f}"
    #no matches found, return max precision
    #no matches found, return max precision string
    return f"{number:.{max_precision}f}"
