
import csv
from constants import ___CSV_CAULDRON____, ___PREFERRED_RESOURCES___, ___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___, ___PREFERRED_RESOURCES_EXTENDED___
from utility import print_variables
from utility import format_precision



def calculate_cauldron(resource, usage_level = 0):
    #create the cauldron object
    cauldron = cauldron_object(usage_level)
    #determine the combination
    cauldron.determine_combinations(resource)



#base cauldron object
class cauldron_object(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, usage_level=0):
        #self.inputs = all possible inputs (dict of resource (key) and their value (key))
        #self.outputs = all possible outputs (dict of resource (key) and their values (keys))
        self.get_in_and_outputs()
        #preferred inputs (array of resource names)
        self.preferred_inputs = self.get_preferred_inputs(usage_level)
        


    def get_preferred_inputs(self, usage_level=0):
        #inputs is a dict of: resource name with no value
        list = {}
        #for each preferred resource
        for resource_name in ___PREFERRED_RESOURCES___.keys():
            #add the name to the list
            list[resource_name] = ""
        #if extend list is also to be used
        if usage_level == 1:
            #for each preferred resource
            for resource_name in ___PREFERRED_RESOURCES_EXTENDED___.keys():
                #add the name to the list
                list[resource_name] = ""
        #if all inputs should be used
        if usage_level > 1:
            #for each input
            for resource_name in self.inputs.keys():
                #add the name to the list
                list[resource_name] = ""
        #return the list (only the keys)
        return list.keys()



    #self.inputs = all possible inputs (dict of resource (key) and their value (key))
    #self.outputs = all possible outputs (dict of resource (key) and their values (keys))
    #ouputs is a dict of: key: name, values (dict): target_value, multiplier, heat_cost
    def get_in_and_outputs(self):
        #initialize variables
        self.inputs = dict()
        self.outputs = dict()
        #use the database
        with open(___CSV_CAULDRON____) as csvfile: 
            #use a dict
            reader = csv.DictReader(csvfile)
            #try
            try:
                #for each row
                for row in reader:
                    #get data
                    resource = row["resource"]
                    #data for inputs
                    value = row["value"]
                    #if data has been set
                    if resource != None and value != None:
                        #add to input
                        self.inputs[resource] = float(value)
                    #data for outputs
                    target_value = row["target_value"]
                    multiplier = row["multiplier"]
                    heat_cost = row["heat_need"]
                    #if data has been set (expect heat need)
                    if target_value != None and multiplier != None:
                        #add to output
                        self.outputs[resource] = {"target_value":float(target_value), "multiplier": float(multiplier), "heat_cost": heat_cost}
            #if exception
            except csv.Error as e:
                #return the error
                return None, 'file {}, line {}: {}'.format(___CSV_CAULDRON____, reader.line_num, e)   
    



    def determine_combinations(self, resource):
        #check for matching name
        resource = self.correct_resource_name(resource)
        #dict of combinations
        combinations = dict()
        #normal cauldron = 3 inputs
        #for the first resource
        for resource_1 in self.preferred_inputs:
            #the same as the resource we are looking for
            if resource_1 == resource:
                #skip
                continue
            for resource_2 in self.preferred_inputs:
                #the same as the resource we are looking for
                if resource_2 == resource:
                    #skip
                    continue
                for resource_3 in self.preferred_inputs:
                    #the same as the resource we are looking for
                    if resource_3 == resource:
                        #skip
                        continue
                    determined_output = self.determine_output(resource_1, resource_2, resource_3)
                    #print(f"Looking for '{resource}', found '{determined_output}' using {[resource_1, resource_2, resource_3]}")
                    #if the output is the same as the wanted output
                    if resource == determined_output:
                        #calculate the fertilizer cost
                        cost_fertilizer = self.get_fertilizer_cost(resource_1, resource_2, resource_3)
                        #calculate the heat cost
                        cost_heat = self.get_heat_cost([resource, resource_1, resource_2, resource_3])
                        #sort the resources to always get the same name, no matter of the resource placement
                        resources = sorted([resource_1, resource_2, resource_3])
                        #create name
                        name = f"{resources[0]}, {resources[1]}, {resources[2]}"
                        #if combination not yet present
                        if name not in combinations:
                            #add to the list
                            combinations[name] = [cost_fertilizer, cost_heat, name]
        #only get the values
        combination_list = combinations.values()
        #sort on fertilizer cost
        combination_list_fertilizer = sorted(sorted(combination_list, key=lambda combination: combination[1]), key=lambda combination: combination[0])
        #sorted(combination_list, key=lambda combination: combination[0])
        #
        #sort on heat cost
        combination_list_heat = sorted(sorted(combination_list, key=lambda combination: combination[0]), key=lambda combination: combination[1])
        #
        #sorted(combination_list_fertilizer, key=lambda combination: combination[1])
        #print combinations
        print(f"Found {len(combination_list)} combinations for '{resource}', requiring a base heat of {self.get_heat_cost([resource]):.0f}")
        print(f"Lowest fertilizer:")
        #keep track of index
        index = 1
        #for each combination
        for combination in combination_list_fertilizer:
            #print(f"combination: '{combination}'")
            print(f"fertilizer: {combination[0]:.2f}, heat: {combination[1]:.0f}, inputs: {combination[2]}")
            #if index is equal or exceeding the amount preferred to be shown
            if index >= ___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___:
                #limit reached, stop
                break
            #limit not yet reached
            else:
                #up the index
                index += 1
        print(f"Lowest heat:")
        #keep track of index
        index = 1
        #for each combination
        for combination in combination_list_heat:
            #print(f"combination: '{combination}'")
            print(f"fertilizer: {combination[0]:.2f}, heat: {combination[1]:.0f}, inputs: {combination[2]}")
            #if index is equal or exceeding the amount preferred to be shown
            if index >= ___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___:
                #limit reached, stop
                break
            #limit not yet reached
            else:
                #up the index
                index += 1



    def correct_resource_name(self, resource):
        #variable to keep track of matches
        matches = []
        #check exact match (?)
        for entry in self.outputs.keys():
            #if exact match
            if resource == entry:
                #stop
                return resource
            #if partial match
            if resource in entry:
                #add to the list
                matches.append(entry)
        #if 1 matche found
        if len(matches) == 1:
            #indicate mapping
            print(f"mapped '{resource}' to '{matches[0]}'")
            #return the only match
            return matches[0]
        #multiple matches found
        elif len(matches) > 1:
            #print message
            print(f"Multiple matches found for resource: '{resource}' => '{matches}'")
            #stop
            exit()
        #no matches found
        else:
            #print message
            print(f"No matches found for resource: '{resource}'")
            #stop
            exit()



    def get_fertilizer_cost(self,resource_1, resource_2, resource_3):
        #initialize value
        fertilizer_cost = 0.0
        #convert to list
        list = [resource_1, resource_2, resource_3]
        #for entry in list
        for entry in list:
            #check in preferred resources
            if entry in ___PREFERRED_RESOURCES___:
                #get the cost
                cost = ___PREFERRED_RESOURCES___[entry]
                #add to the total cost
                fertilizer_cost += float(cost)
            #check in preferred resources extended
            elif entry in ___PREFERRED_RESOURCES_EXTENDED___:
                #get the cost
                cost = ___PREFERRED_RESOURCES_EXTENDED___[entry]
                #add to the total cost
                fertilizer_cost += float(cost)
            else:
                #rint(f"could not find fertilizer cost for '{resource_1}'")
                pass
        #return the cost
        return fertilizer_cost



    def get_heat_cost(self, resources):
        #initialize value
        heat_cost = 0.0
        #for entry in list
        for entry in resources:
            #if value in outputs (thus having a heat cost)
            if entry in self.outputs.keys():
                #get the heat cost of the entry
                cost = self.outputs[entry]["heat_cost"]
                #if the cost is set 
                if cost != None and cost != "":
                    #add to heat cost
                    heat_cost += float(cost)
        #return the heat cost
        return heat_cost
        


    def determine_output(self, resource_1, resource_2, resource_3):
        #get the score
        score = self.calculate_score(resource_1, resource_2, resource_3)
        #list to keep track of all calculated distances
        output_distances = []
        #for every possible output
        for output_name, output in self.outputs.items():
            #calculate distance
            distance = abs(output["target_value"] - score) * output["multiplier"]
            #save distance and name to list
            output_distances.append([distance, output_name])
        #sort list (smallest first)
        output_distances = sorted(output_distances)
        #return the first output's name
        return output_distances[0][1]
    


    def calculate_score(self, resource_1, resource_2, resource_3):
        #get the value
        value_1 = self.inputs[resource_1]
        #get the value
        value_2 = self.inputs[resource_2]
        #get the value
        value_3 = self.inputs[resource_3]
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


