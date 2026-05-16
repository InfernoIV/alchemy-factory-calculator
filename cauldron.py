
import csv
from constants import ___CSV_CAULDRON____

def get_cauldron_name(resource):
    #value to return
    target_resource = ""
    #check for all the same recipes to capture all output
    with open(___CSV_CAULDRON____) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        #try
        try:
            #for each row
            for row in reader:
                #get the resource name
                resource_name = row["resource"]
                #check only for fuzzy matching recipe names
                if resource in resource_name:
                    #if we already found something before
                    if target_resource != "":
                        #return terror
                        return None, f"Found multiple values found for '{resource}'"
                    #save the resource name
                    target_resource = resource_name
                #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)
    #if we found a name
    if target_resource != "":
        #return it
        return target_resource, None
    #nothing found
    return None, f"No resource found for '{resource}'"



def get_cauldron_target(resource):
    #target value
    target_value = 0
    #previous value
    previous_value = 0
    #next value
    next_value = 0

    #get the actual value first
    #check for all the same recipes to capture all output
    with open(___CSV_CAULDRON____) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        #try
        try:
            #for each row
            for row in reader:
                #if match found
                if resource == row["resource"]:
                    #save the value
                    target_value = row["target_value"]
                    #check if feasable
                    if target_value == None:
                        #return error
                        return None, None, f"No cauldron recipe possible for {resource}"
                    #cast to float
                    target_value = float(target_value)
                    #stop looking
                    break
        #if exception
        except csv.Error as e:
            #return the error
            return None, None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)
    #get the min and max
    #check for all the same recipes to capture all output
    with open(___CSV_CAULDRON____) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        #try
        try:
            #for each row
            for row in reader:
                #get the value
                value = row["target_value"]
                #only when it is a value
                if value != None:
                    #cast to float
                    value = float(value)
                    #if lower than target
                    if value < target_value:
                        #save to min
                        previous_value = value
                    #if higher than target
                    elif value > target_value:
                        #save to max
                        next_value = value
                        #stop looking
                        break     
        #if exception
        except csv.Error as e:
            #return the error
            return None, None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)    
    #calculate min
    target_min = float((previous_value+target_value)/2)
    #calculate max
    target_max = float((next_value+target_value)/2)
    #get the target value
    return target_min, target_max, None
    


#base cauldron object
class cauldron_obj(object):
    #placeholder

    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        #placeholder
        pass