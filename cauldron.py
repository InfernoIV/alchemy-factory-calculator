
import csv
from constants import ___CSV_CAULDRON____, ___PREFERRED_RESOURCES___
from utility import print_variables


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
                    #if we have an exact match:
                    if resource == resource_name:
                        #return this
                        return resource_name, None
                    #if we already found something before
                    if target_resource != "":
                        #return terror
                        return None, f"Found at least values found for '{resource}': '{target_resource}', '{resource_name}'"
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
    target_value = float(0)
    #previous value
    previous_value = float(0)
    #next value
    next_value = float(0)

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
                        return None, f"No cauldron recipe possible for {resource}"
                    #cast to float
                    target_value = float(target_value)
                    #stop looking
                    break
        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)
    #debug
    #print(f"target: {target_value}")
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
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)    
    #calculate min
    target_min = float((previous_value+target_value)/2)
    #if previous was not set
    if previous_value == float(0):
        #set to bottom
        target_min = float(0)
    #calculate max
    target_max = float((next_value+target_value)/2)
    #if max not set
    if next_value == float(0):
        #set to max value
        target_max = float('inf')
    #create cauldron object
    cauldron = cauldron_obj(resource, target_min, target_max)
    #get the target value
    return cauldron, None
    


def get_cauldron_resources():
    #list to return
    resource_list = dict()
    #check for all the same recipes to capture all output
    with open(___CSV_CAULDRON____) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        #try
        try:
            #for each row
            for row in reader:
                #add to list (resource, value)
                resource_list[row["resource"]] = float(row["value"])
        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)  
    #return list
    return resource_list, None



#base cauldron object
class cauldron_obj(object):
    #list of resources, read and saved from the csv
    resources = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, resource, min, max):
        #set resource
        self.resource = str(resource)
        #set min
        self.min = float(min)
        #set max
        self.max = float(max)



    def calc_possiblities(self, only_preffered=False):
        #get resources
        self.retrieve_resources()
        #clear list
        self.possiblities = []
        #get preferred combinations
        self.get_combinations(___PREFERRED_RESOURCES___)
        #print(f"self.possiblities (preferred): '{self.possiblities}'")
        #if we did not find any preferred combinations
        if self.possiblities == [] and only_preffered == False:
            #get other combinations
            self.get_combinations(self.resources.keys())      
            #print(f"self.possiblities (normal): '{self.possiblities}'")
        #sort the list
        #sorted(self.possiblities, key=lambda score: self.possiblities[0])
        #return the list
        return self.possiblities



    def retrieve_resources(self):
        #if resource are not yet retrieved
        if self.resources == []:
            #get the resources
            resources, error = get_cauldron_resources()
            #check for error
            if error != None:
                #return the error
                return error
            #copy the resources over
            self.resources = resources



    def get_combinations(self, resource_list):
        for resource_1 in resource_list:
            #check for target resources (no usefull)
            if resource_1 == self.resource:
                #next
                continue
            #get the value
            value_1 = self.resources[resource_1]
            #second resource
            for resource_2 in resource_list:
                #check for target resources (no usefull)
                if resource_2 == self.resource:
                    #next
                    continue
                #get the value
                value_2 = self.resources[resource_2]
                #third resource
                for resource_3 in resource_list:
                    #check for target resources (no usefull)
                    if resource_3 == self.resource:
                        #next
                        continue
                    #get the value
                    value_3 = self.resources[resource_3]
                    #calculate multiplier (1, 0.65, 0.5)
                    multiplier = 1
                    #if all the same resources
                    if resource_1 == resource_2 and resource_1 == resource_3:
                        #multiplier is lowest
                        multiplier = 0.5
                    #if only 2 the same resources
                    elif resource_1 == resource_2 or resource_1 == resource_3 or resource_2 == resource_3:
                        #multiplier is lower
                        multiplier = 0.65
                    #check the score
                    score = float(((value_1 + value_2 + value_3) * int(multiplier*100))/100)
                    #debug
                    #print(f"score: '{score}', multiplier: '{multiplier}'{resource_1:value_1},{resource_2:value_2},{resource_3:value_3}")
                    print_variables(score, multiplier, resource_1, value_1, resource_2, value_2, resource_3, value_3)
                    #if within target
                    if self.min <= score <= self.max:
                        #add to the list
                        self.possiblities.append([resource_1, resource_2, resource_3])
        #remove duplicate recipes
        self.remove_duplicate_recipes()



    def remove_duplicate_recipes(self):
        #list to keep track of unique recipes
        unqiue_recipes = []
        #for all the available recipes
        for recipe in self.possiblities:
            #sort
            sorted_recipe = sorted(recipe)
            #if recipe is not yet found
            if sorted_recipe not in unqiue_recipes:
                #add to list
                unqiue_recipes.append(sorted_recipe)
        #only save the unique recipes
        self.possiblities = unqiue_recipes

    def describe_target(self):
        #print self
        print(f"Cauldron target '{self.resource}' is between '{self.min}' and '{self.max}'")
    
    

    def describe_possiblities(self):
        #header
        print(f"Cauldron possiblities ({len(self.possiblities)}):")
        #for each entry
        for possibility in self.possiblities[:100]:
            #print the possiblity
            print(f"{", ".join(possibility)}")


