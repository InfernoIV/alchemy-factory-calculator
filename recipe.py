import csv, math
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
            #if the list is empty
            if len(recipes) == 0:
                #no recipes found
                return None, None
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
                #multiple recipes found
                return None, f"Multiple recipes found, but no preffered recipe! '{recipes}'"
    #no recipes found
    return None, None



def get_recipe_list(resource):
    #list to store information into
    recipe_list = []
    #collect recipes
    collect_recipe_list(recipe_list, resource)
    #return the list
    return recipe_list



def collect_recipe_list(recipe_list, resource, amount=0):
    #recipe variable
    recipe = None
    #error variable
    error = None
    #check if we need to scale
    if amount == 0:
        #get the recipe
        recipe, error = get_recipe(resource)
    else:
        #get a scaled recipe
        recipe, error = scale_recipe(resource, amount)
    #check error
    if error != None: return
    #if there is a recipe
    if recipe != None:
        #add recipe to the list
        recipe_list.append(recipe)
        #for each input
        for input, input_amount in recipe.inputs.items():
            #unscaled
            if amount == 0:
                #dig deeper
                collect_recipe_list(recipe_list, input)
            #scaled
            else:
                #dig deeper
                collect_recipe_list(recipe_list, input, input_amount)
        


def get_recipe_dict(resource):
    #list to store information into
    recipe_dict = {}
    #collect recipes
    error = collect_recipe_dict(recipe_dict, resource)
    #return the list
    return recipe_dict, error



def collect_recipe_dict(recipe_dict, resource, amount=0):
    #recipe variable
    recipe = None
    #error variable
    error = None
    #check if we need to scale
    if amount == 0:
        #get the recipe
        recipe, error = get_recipe(resource)
    else:
        #get a scaled recipe
        recipe, error = scale_recipe(resource, amount)
    #check error
    if error != None: 
        #return the rror
        return error
    #if there is a recipe
    if recipe != None:
        #add recipe to the list
        recipe_dict[recipe.name] = recipe
        #for each input
        for input, input_amount in recipe.inputs.items():
            #unscaled
            if amount == 0:
                #dig deeper
                collect_recipe_list(recipe_dict, input)
            #scaled
            else:
                #dig deeper
                collect_recipe_list(recipe_dict, input, input_amount)
    #no recipe found (which can happen)
    return None



def scale_recipe(resource, amount):
    #get the recipe
    recipe, error = get_recipe(resource)
    #check for error
    if error != None:
        #return error
        return None, error
    #if there is a recipe
    if recipe != None:
        #do stuff
        recipe.scale_to_amount_resource(resource, amount)
        #return the recipe
        return recipe, None
    #no recipe
    return None, None



#calculates the recipe tree
def calculate_recipe(resource, amount):
    #recipe dictionary that is used
    recipe_dict = {}
    #create dictionary for the need
    resource_need = {resource: float(amount)}
    #create dictionary for the output
    resource_extra = {}
    #start the chain
    error = calculate_dependency(recipe_dict, resource_need, resource_extra)
    #check for error
    if error != None:
        return None, None, None, error
    #return the recipes
    return recipe_dict, resource_need, resource_extra, None



#calculate the depency recipes
def calculate_dependency(recipe_dict, resource_need, resource_extra, depth=0):
    #for the leftover need
    for resource, amount in dict(resource_need).items():
        #get the recipe
        recipe, error = scale_recipe(resource, float(amount))                      
        #check error
        if error != None:
            #return the error
            return error
        if recipe != None:
            #add the depth
            recipe.depth = depth
            #add to the dictionary
            recipe_dict[recipe.name] = recipe
            #for every needed input
            for input, input_amount in recipe.inputs.items():
                #if there already is a need
                if input in resource_need:
                    #add to the existing
                    resource_need[input] += float(input_amount)
                #if there is not yet a need
                else:
                    #add a new entry
                    resource_need[input] = float(input_amount)
            #for every output
            for output, output_amount in recipe.outputs.items():
                #if we have a need for this resource
                if output in resource_need:
                    #get the extra amount
                    need_amount = resource_need[output]           
                    #check if we create exactly the need
                    if float(output_amount) == need_amount:
                        #remove the need
                        resource_need.pop(resource)
                    #we create more than we need
                    elif float(output_amount) > need_amount:
                        #remove the need
                        resource_need.pop(output)
                        #add the leftover to the by-product
                        left_over = float(output_amount) - need_amount
                        #if entry exists
                        if output in resource_extra:
                            #add to this entry
                            resource_extra[output] += left_over
                        #no entry exists
                        else:
                            #create the entry
                            resource_extra[output] = left_over
                    #we create less than the need (shouldn't happen?)
                    else:
                        #reduce the need
                        resource_need[output] -= output_amount
                        #return an error for now
                        #return f"Too little production! '{recipe.outputs}' '{resource_need}'"
                #otherwise this is a by-product
                else:
                    #if an entry already exists
                    if output in resource_extra:
                        #add to this entry
                        resource_extra[output] += output_amount
                    #entry does not exist
                    else:
                        #create the entry
                        resource_extra[output] = output_amount
        #no recipe found
        else:
            #debug
            #print(f"no recipe found for : '{resource}', removing")
            #remove the resource from the list to prevent infinite loops
            resource_need.pop(resource)
    #if there is still a resource need
    if len(resource_need) > 0:
        #go deeper
        calculate_dependency(recipe_dict, resource_need, resource_extra, depth+1)
    #return no error
    return None



#looks up the recipe and returns it (in the same format)
def lookup_recipe(filename, filter):
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
                    recipe_name = f"{row["output-resource"]} (cauldron)"
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
                                inputs[resource] += float(amount)
                            #no entry
                            else:
                                #add data to inputs
                                inputs[resource] = float(amount)
                        #add the output
                        outputs[output_resource] = float(amount)
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
                                            #set the change to a float
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
    #name of the recipe
    name = ""
    #list of inputs of the recipe
    inputs_base = []
    #list of outputs of the recipe
    outputs_base = []
    #keep track of scaled inputs
    inputs = []
    #keep track of scaled outputs
    outputs = []
    #time of the recipe
    time = 60
    #name of the used device
    device = ""
    #amount of devices
    device_amount = 1
    #depth, for reporting purposes
    depth = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, inputs, outputs, time, device, depth=0):
        #save name
        self.name = str(name)
        #save inputs
        self.inputs_base = inputs
        #save outputs
        self.outputs_base = outputs
        #save time
        self.time = float(time)
        #save device name
        self.device = str(device)
        #scale to 60s
        self.scale_to_time()
        #set depth
        self.depth = depth


    #function that is returned 
    def __repr__(self):
        #return self as dictionary
        return f"recipe: '{str(self.__dict__)}'"
    


    #scale all inputs and outputs to a specific time
    def scale_to_time(self, time=float(60)):
        #calculate the time factor
        time_factor = time/self.time
        #set time
        self.time = time
        #for each input
        for input in self.inputs_base:
            #adjust the inputs
            self.inputs_base[input] = float(self.inputs_base[input]) * time_factor
        #for each input
        for output in self.outputs_base:
            #adjust the inputs
            self.outputs_base[output] = float(self.outputs_base[output]) * time_factor
        #copy the values to scaled input
        self.inputs = self.inputs_base
        #copy the values to scaled output
        self.outputs = self.outputs_base



    #scale the number of devices to get the needed amount
    def scale_to_amount_resource(self, resource, amount):
        #get amount per device
        base_amount = self.outputs[resource]
        #calculate the needed device amount
        device_amount = math.ceil(amount / base_amount)
        #scale the recipe
        self.scale_to_amount_devices(device_amount)



    #scale the input and output to the number of devices
    def scale_to_amount_devices(self, device_amount):
        #amount of devices
        self.device_amount = device_amount
        #scale inputs
        for input, input_amount in self.inputs_base.items():
            #adjust the input
            self.inputs[input] = device_amount * input_amount
        #scale inputs
        for output, output_amount in self.outputs_base.items():
            #adjust the input
            self.outputs[output] = device_amount * output_amount



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
        string += f"{self.device_amount} {self.device} => "
        
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


