
import csv
from constants import ___CSV_CAULDRON____



def check_cauldron_target(resource):
    #variable to return
    target_value = float(0)
    #resource name to return
    target_resource = ""
    #flag to indicate found (and to check for multiple recipes (due to fuzzy input management))
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
                        return None, None, f"Found multiple values for '{resource}'"
                    #set flag that something is found
                    target_resource = resource_name
                    #get the target value
                    value = row["target_value"]
                    #check if set
                    if value != None:
                        #convert to number
                        target_value = float(value)
        #if exception
        except csv.Error as e:
            #return the error
            return None, None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)
    #get the target value
    return target_resource, target_value, None
    


#base cauldron object
class cauldron_obj(object):
    #placeholder

    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        #placeholder
        pass