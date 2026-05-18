
import csv
from constants import ___CSV_CAULDRON____, ___PREFERRED_RESOURCES___, ___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___, ___PREFERRED_RESOURCES_EXTENDED___
from utility import print_variables
from utility import format_precision

def get_cauldron_name(resource):
    #check for exact match
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
                #if we have an exact match:
                if resource == resource_name:
                    #return this
                    return resource_name, None
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)
    #check for fuzzy match
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
    #target multiplier
    target_multiplier = float(0)
    #previous value
    previous_value = float(0)
    #previous multplier
    previous_multiplier = float(0)
    #next value
    next_value = float(0)
    #next multiplier
    next_multiplier = float(0)

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
                    #get multiplier
                    target_multiplier = row["multiplier"]
                    #check if feasable
                    if target_multiplier == None:
                        #return error
                        return None, f"No cauldron recipe possible for {resource}"
                    #cast to float
                    target_multiplier = float(target_multiplier)
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
                #get the multiplier
                mutliplier = row["multiplier"]
                #only when it is a value
                if value != None:
                    #cast to float
                    value = float(value)
                    #if lower than target
                    if value < target_value:
                        #save to min
                        previous_value = value
                        #save the multiplier
                        previous_multiplier = mutliplier
                    #if higher than target
                    elif value > target_value:
                        #save to max
                        next_value = value
                        #save the multiplier
                        next_multiplier = mutliplier
                        #debug
                        #print(f"previous = '{previous_value}' * '{previous_multiplier}', target = '{target_value}' * '{target_multiplier}', next = '{next_value}' * '{next_multiplier}'")
                        #stop looking
                        break     
        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)    
    #put the value in the middle
    target_min = previous_value
    #go through calculations
    while True:
        #calculate the previous distance
        previous_distance = float(abs(target_min - previous_value)) * float(previous_multiplier)
        #calculate the target distance
        target_distance = float(abs(target_min - target_value)) * float(target_multiplier)
        #if the target distance is closer
        if target_distance < previous_distance:    
            #stop
            break
        #otherwise up the value
        target_min += 1
    #put the value in the middle
    target_max = next_value
    #go through calculations
    while True:
        #calculate the previous distance
        next_distance = float(abs(target_max - next_value)) * float(next_multiplier)
        #calculate the target distance
        target_distance = float(abs(target_max - target_value)) * float(target_multiplier)
        #debug
        #print(f"target_distance: '{target_distance}', next_distance: '{next_distance}'")
        #if the target distance is closer
        if target_distance < next_distance:
            #stop
            break
        #otherwise down the value
        target_max -= 1
    #create cauldron object
    cauldron = cauldron_obj(resource, target_value, target_multiplier, previous_value, previous_multiplier, next_value, next_multiplier)
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



def get_heat_cost(resource):
#check for all the same recipes to capture all output
    with open(___CSV_CAULDRON____) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        #try
        try:
            #for each row
            for row in reader:
                #if we have an exact match:
                if resource == row["resource"]:
                    #return this
                    heat_need = row["heat_need"]
                    #check if we can calulate
                    if heat_need != None and heat_need != "":
                        #return the head need
                        return float(heat_need), None
                    else:
                        #cannot crafting using cauldron
                        return 0, None
                #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)
    #no entry found
    return None, "No resource found!"



#base cauldron object
class cauldron_obj(object):
    #list of resources, read and saved from the csv
    resources = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, resource, target_value, target_multiplier, previous_value, previous_multiplier, next_value, next_multiplier):
        #set resource
        self.resource = str(resource)
        #save the data
        self.target_value = target_value
        self.target_multiplier = target_multiplier
        self.previous_value = previous_value
        self.previous_multiplier = previous_multiplier
        self.next_value = next_value
        self.next_multiplier = next_multiplier

    def calc_possiblities(self, only_preffered=False):
        #get resources
        self.retrieve_resources()
        #clear list
        self.possiblities = []
        #get preferred combinations
        self.get_combinations(___PREFERRED_RESOURCES___.keys())
        #check for extended combinations
        self.get_combinations(___PREFERRED_RESOURCES_EXTENDED___.keys())
        #if we did not find any preferred combinations
        if self.possiblities == [] and only_preffered == False:
            #get other combinations
            self.get_combinations(self.resources.keys())      
            #print(f"self.possiblities (normal): '{self.possiblities}'")
        #remove duplicate recipes
        self.remove_duplicate_recipes()
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
            #second resource
            for resource_2 in resource_list:
                #check for target resources (no usefull)
                if resource_2 == self.resource:
                    #next
                    continue
                #third resource
                for resource_3 in resource_list:
                    #check for target resources (no usefull)
                    if resource_3 == self.resource:
                        #next
                        continue
                    #get the score
                    score = self.calculate_score(resource_1, resource_2, resource_3)
                    #if within target
                    if self.check_within_target(score):
                        #add to the list
                        self.possiblities.append([resource_1, resource_2, resource_3])



    def check_within_target(self, score):
        #calculate distance to target 
        target_distance = float(abs(score - self.target_value)) * float(self.target_multiplier)
        #get the distance to the previous
        previous_distance = float(abs(score - self.previous_value)) * float(self.previous_multiplier)
        #get the distance to the next
        next_distance = float(abs(score - self.next_value)) * float(self.next_multiplier)
        #return if target distance is smaller than the neighbours
        return target_distance < previous_distance and target_distance < next_distance



    def calculate_score(self, resource_1, resource_2, resource_3):
        #get the value
        value_1 = self.resources[resource_1]
        #get the value
        value_2 = self.resources[resource_2]
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
        #return the score
        return score

    

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
        #clear possibilities
        self.possiblities = []
        #get heat cost for this resource (base heat cost)
        cost_heat, _ = get_heat_cost(self.resource)
        #for each entry
        for possibility in unqiue_recipes:
            #initialize cost
            cost_fertilzier = 0.0
            #for each resource
            for entry in possibility:
                #get the heat cost (if applicable)
                cost_heat_component, error = get_heat_cost(entry)
                #check for error
                if error != None:
                    #return the error
                    return error
                #if not set
                if cost_heat_component == None:
                    #set to 0
                    cost_heat_component = 0
                #add heat cost
                cost_heat += cost_heat_component

                if entry in ___PREFERRED_RESOURCES___:
                    #add the cost
                    cost_fertilzier += float(___PREFERRED_RESOURCES___[entry])
                #check extended list
                elif entry in ___PREFERRED_RESOURCES_EXTENDED___:
                    #add the cost
                    cost_fertilzier += float(___PREFERRED_RESOURCES_EXTENDED___[entry]) 
            #add to the list of possibilities
            self.possiblities.append([cost_fertilzier, cost_heat, possibility])
        #sort on fertilizer cost
        self.possiblities = sorted(self.possiblities, key=lambda possibility: possibility[0])
        #sort on heat cost
        self.possiblities = sorted(self.possiblities, key=lambda possibility: possibility[1])


    def describe_target(self):
        heat_need,error = get_heat_cost(self.resource)
        #print self
        print(f"Cauldron target '{self.resource}' requires a base heat need of {heat_need}")
    
    

    def describe_possiblities(self):
        #header
        print(f"Cauldron possiblities ({len(self.possiblities)}):")
        #for each entry
        for possibility in self.possiblities[:___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___]:
            score = self.calculate_score(possibility[2][0], possibility[2][1], possibility[2][2])# resource_1, resource_2, resource_3
            #print the possiblity
            print(f"fertilizer: {possibility[0]:.2f}, heat: {format_precision(possibility[1])}, inputs: {", ".join(possibility[2])}")


