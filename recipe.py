import csv
from constants import ___CSV_RECIPES_CAULDRON____, ___CSV_RECIPES____,___PREFERRED_RECIPES___



#function to receive a single recipe
def get_recipe(resource):
    #print(f"Looking for resource '{resource}'")
    #create filter to search for
    filter = {"output-resource": resource}
    #search for cauldron recipe
    cauldron_recipe, error = lookup_recipe(___CSV_RECIPES_CAULDRON____, filter)
    #print(f"cauldron_recipe: {cauldron_recipe}")
    #check for errors
    if error != None:
        #return the error
        return None, error
    #cauldron recipe found
    if len(cauldron_recipe) > 0:
        #if multiple recipes found
        if len(cauldron_recipe) > 1:
            #indicate issue
            return None, f"ERROR: multiple cauldron recipes: {cauldron_recipe}"
        #return the cauldron recipe, should only be 1 (so take the first index)
        return cauldron_recipe[0], None
    #search for normal recipe
    else:
        #get the normal recipes
        recipes, error = lookup_recipe(___CSV_RECIPES____, filter)
        #print(f"recipes: {recipes}")
        #if error
        if error != None:
            #return the error
            return None, error
        #if any recipe found
        if recipes != None:
            #if only a single recipe found
            if len(recipes) == 1:
                #return this recipe
                return recipes[0], None
            #multiple recipes found
            else:
                #for each recipe
                for recipe in recipes:
                    #if a favorite recipe is found
                    if recipe.name in ___PREFERRED_RECIPES___:
                        #return the recipe
                        return recipe, None
    #no recipes found
    return None, "No recipe found!"


def get_recipe_list(resource):
    #list to store information into
    recipe_list = []
    #collect recipes
    collect_recipes(recipe_list, resource)
    #return the list
    return recipe_list


def collect_recipes(recipe_list, resource):
    #get the recipe
    recipe, error = get_recipe(resource)
    #check error
    if error != None: return
    #if there is a recipe
    if recipe != None:
        #add recipe to the list
        recipe_list.append(recipe)
        #for each input
        for input, input_amount in recipe.inputs.items():
            #dig deeper
            collect_recipes(recipe_list, input)
        


#calculates the recipe tree
def calculate_recipe(resource, amount):
    #get the recipe
    recipe = get_recipe(resource)
    #if there is a recipe
    if recipe != None:
        #do stuff
        pass



#looks up the recipe and returns it (in the same format)
def lookup_recipe(filename, filter):
    #print(f"filter: '{filter}'")
    #list of recipes
    matching_recipes = []
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        #try
        try:
            #for each row
            for row in reader:
                #check filters
                flag_match = True
                #for all filters
                for field, contains in filter.items():
                    #check if not matching
                    if contains.lower() != row[field].lower():
                        #no match!
                        flag_match = False
                #if still valid
                if flag_match:
                    #check device name to determine if it is a cauldron recipe
                    device = row.get("device")
                    #default to cauldron recipe
                    recipe_name = f"{row["output-resource"]} (Cauldron)"
                    #inputs
                    inputs = {}
                    #outputs
                    outputs = {}
                    #time
                    time = 60
                    #output resource, for easy reference
                    output_resource = row["output-resource"]

                    #if cauldron recipe
                    if device == None:
                        #set device to cauldron
                        device = "cauldron"
                        #get the amount
                        amount = row["amount"]
                        #get the max 3 inputs
                        for i in range(1,4):
                            #get the resource name
                            resource = row[f"input-{i}-resource"]
                            #already an entry
                            if inputs.get(resource) != None:
                                #add the amount to the existing amount
                                inputs[resource] += amount
                            #no entry
                            else:
                                #add data to inputs
                                inputs[resource] = amount
                        #add the output
                        outputs[output_resource] = (1, amount)
                            

                    #normal recipe
                    else:
                        #get the name
                        recipe_name = row["recipe-name"]
                        #get the time
                        time = row["time"]
                        #get the max 9 inputs
                        for i in range(1,10):
                            #get the resource name
                            resource = row[f"input-{i}-resource"]
                            #if no data
                            if resource == "" or resource == None:
                                #stop looking for data
                                break
                            #add data to inputs
                            inputs[resource] = float(row[f"input-{i}-amount"])
                        #check for all the same recipes to capture all output
                        with open(filename) as csvfile: 
                            #use a dict
                            reader = csv.DictReader(csvfile)
                            #try
                            try:
                                #for each row
                                for row in reader:
                                    #check only for matching recipe names
                                    if row["recipe-name"] == recipe_name:
                                        #get the chance
                                        chance = row["chance"]
                                        #if chance is not set
                                        if chance == None or chance == "":
                                            #set to 100%
                                            chance = 1
                                        else:
                                            chance = float(chance)/float(100)
                                        #get the amount
                                        amount = float(row["output-amount"])
                                        #add the output with chance
                                        outputs[row["output-resource"]] = chance * amount
                            #if exception
                            except csv.Error as e:
                                #return the error
                                return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)
                    #create recipe object
                    recipe = recipe_obj(recipe_name, inputs, outputs, time, device)
                    #add recipe to the list
                    matching_recipes.append(recipe)
        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)
    #return the list of matching recipes
    return matching_recipes, None 



#base recipe object
class recipe_obj(object):
    
    name = ""
    inputs = []
    outputs = []
    time = 60
    device = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, inputs, outputs, time, device):
        self.name = str(name)
        self.inputs = inputs
        self.outputs = outputs
        self.time = float(time)
        self.device = str(device)

        #scale to 60s
        self.scale_to_time()


    def __repr__(self):
        return f"recipe: '{str(self.__dict__)}'"
    


    #scale all inputs and outputs to a specific time
    def scale_to_time(self, time=float(60)):
        #calculate the time factor
        time_factor = time/self.time
        #set time
        self.time = time
        #for each input
        for input in self.inputs:
            #adjust the inputs
            self.inputs[input] = float(self.inputs[input]) * time_factor
        #for each input
        for output in self.outputs:
            #adjust the inputs
            self.outputs[output] = float(self.outputs[output]) * time_factor
    
    
    #returns a string with a description
    def description(self):
        #start with the device description
        string = f"{self.device}"
        #inputs
        inputs = ""
        #for each input
        for input, amount in self.inputs.items():  
            #if already input existing
            if inputs != "":
                #add comma
                inputs += ", "
            inputs += f"{format_precision(amount)} {input}"
        #if there was an input
        if inputs != "":
            string += f" uses {inputs} to create "
        else:
            string += "creates "
        #output string
        outputs = ""
        #for each input
        for output, amount in self.outputs.items():  
            #if already input existing
            if outputs != "":
                #add comma
                outputs += ", "
            #add output
            outputs += f"{format_precision(amount)} {output}"
        #complete the string
        string += outputs
        #return the string
        return string
    
#returns a string with a description
    def description_fast(self):
        #start with the device description
        string = ""
        #inputs
        inputs = ""
        #for each input
        for input, amount in self.inputs.items():  
            #if already input existing
            if inputs != "":
                #add comma
                inputs += ", "
            inputs += f"{format_precision(amount)} {input}"
        #if there was an input
        if inputs != "":
            string += f"{inputs} => "
        string += f"{self.device} => "
        
        #output string
        outputs = ""
        #for each input
        for output, amount in self.outputs.items():  
            #if already input existing
            if outputs != "":
                #add comma
                outputs += ", "
            #add output
            outputs += f"{format_precision(amount)} {output}"
        #complete the string
        string += outputs
        #return the string
        return string

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