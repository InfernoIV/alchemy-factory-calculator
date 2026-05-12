import sys
import math



#base recipe object
class recipe(object):
    #name of the recipe
    name = ""
    #output resource
    output = ""
    #amount of resource
    amount = 0
    #time of the recipe
    time = 0
    #name of the device that is used
    device_name = ""
    #number of the devices used
    device_amount = 1
    #inputs for this recipe
    inputs = {}
    #time factor (to normalize to 60 seconds)
    factor_time = 1
    #
    factor_amount = 1
    #indicating this is a cauldron recipe
    cauldron_recipe = False
    #indication this is a by product
    is_by_product = False
    #chance for this outcome
    chance = 1



    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict, cauldron_recipe = False, is_by_product = False):
        #save if this is a cauldron recipe
        self.cauldron_recipe = cauldron_recipe
        #set flag if this is a by product
        self.is_by_product = is_by_product
        #guard clause flag (to check later)
        flag_guarded = False
        #things to always check
        data_to_check = [
            #we should always have an output
            "output-resource", 
            #there should always be an input
            "input-1-resource", 
        ]
        #if cauldron recipe          
        if self.cauldron_recipe:
            #check for amount
            data_to_check.append("amount")
        #normal recipe
        else:
            #add the other checks
            data_to_check += [
                #there should be a recipe name
                "recipe-name",
                #there should be an output amount
                "output-amount",
                #there should be an time
                "time",
                #there should be an device
                "device"
            ]
        #for each data check
        for entry in data_to_check:
            #if the data does not exist
            if dict[entry] == "":
                #set flag
                flag_guarded = True 
                #indicate missing data
                print(f"Missing {entry}")
        #if there is a guard
        if flag_guarded == True:
            #stop the script
            sys.exit(f"EXITING, dict: {dict}")  
        #data is correct, start conversion to object 
        self.output = dict["output-resource"].lower()
        self.inputs = {}  
        #specifics to cauldron recipe
        if self.cauldron_recipe:
            #cauldron recipes don't have a specific name
            self.name = f"{self.output} (cauldron)"
            #time is always 60
            self.time = 60
            #time factor is then 1
            self.factor_time = 1
            #device is always cauldron
            self.device_name = "cauldron"
            #amount is used for all amounts
            self.amount = float(dict["amount"])
            #for the possible inputs (1-3)
            for i in range(1, 4): 
                #get resource
                resource = dict[f"input-{i}-resource"]
                #add information to list
                self.inputs[resource] = self.amount 
        #specifics to normal recipe
        else:
            #save the recipe name
            self.name = dict["recipe-name"].lower()
            #set device name
            self.device_name = dict["device"].lower()
            #normalize to 60s
            self.time = float(dict["time"])
            #calculate time factor (this also applies to input)
            self.factor_time = 60/self.time
            #re-set the time to 60 s
            self.time = 60
            #get chance (if applicable)
            if dict["chance"] != "":
                #set the chance
                self.chance = int(dict["chance"]) / 100
            #get amount
            amount = float(dict["output-amount"])
            #add the chance factor
            amount *= self.chance          
            #apply time factor to amount
            self.amount = self.factor_time * amount
            #for the possible inputs (1-9)
            for i in range(1, 10): 
                #if entry does not exist
                if f"input-{i}-resource" not in dict.keys():
                    #no more resources: stop
                    break
                #if resource is empty
                if dict[f"input-{i}-resource"] == None or dict[f"input-{i}-amount"] == "":
                    #no more resources: stop
                    break
                else:
                    #get resource
                    resource = dict[f"input-{i}-resource"]
                    #get amount
                    amount = self.factor_time*float(dict[f"input-{i}-amount"])
                    #add information to list
                    self.inputs[resource] = amount



    #function that will print when converted to str
    def __repr__(self):
        #placeholder
        inputs = ""
        #for every input
        for resource, amount in self.inputs.items():
            #if there is alreay something described
            if inputs != "":
                #add a comma
                inputs += ", "
            #add the amount and resource to the string
            inputs += f"{amount:.2f} {resource}"
        #format the string
        string = f"recipe '{self.name}' creates {format_precision(self.amount)} {self.output}"
        #if it is a by-product
        if self.is_by_product:
            #indicate this is a by-product
            string += " as by-product"
        #not a by-product
        else:
            #add device amount and name
            string += f" using {self.device_amount} {self.device_name}"
            #if there are inputs
            if inputs != "":
            #string to return
                string += f" with inputs: {inputs}"
        #return the string
        return string
    


    #function that returns the small description of the recipe
    def get_small_description(self):
        #placeholder variable
        inputs = ""
        #variable for the device
        extention = f"({self.device_amount} {self.device_name})"
        #if this is a by-product
        if self.is_by_product:
            #no extra is input needed
            inputs = "    +"
            #no extra device is needed
            extention = ""
        #not a by-produt
        else:
            #for every input
            for resource, amount in self.inputs.items():
                #string is already filled
                if inputs != "":
                    #add a plus
                    inputs += " + "
                #add the amount and resource to the string 
                inputs += f"{format_precision(amount)} {resource}"
            #if there is input
            if inputs != "":
                #add transformation mark to the string
                inputs += " =>"
        #build the string
        #string = f"{inputs} {self.device_amount} {self.device_name} => {format_precision(self.amount)} {self.output}"
        string = f"{inputs} {format_precision(self.amount)} {self.output} {extention}"
        #return the string
        return string



    #adjust the amount
    def adjust_amount(self, amount):
        #calculate the factor
        self.factor_amount = amount / self.amount
        #set the amount to the needed amount
        self.amount = amount
        #calculate the needed devices
        self.device_amount =  math.ceil(self.device_amount * self.factor_amount)
        #calculate the inputs
        for resource in self.inputs.keys():
            #scale all inputs
            self.inputs[resource] *= self.factor_amount



    #only used for by-products, adjusts the devices
    def adjust_device_amount(self, device_amount):
        #calculate the needed devices
        self.device_amount = device_amount
        #set the amount to the needed amount
        self.amount *= self.device_amount



#function to format a number with a precision
def format_precision(number, max_precision = 2):
    #for 0 to max precision
    for i in range(max_precision+1):
        #check if this precision does not results into a 0 (which means the precision is correct)
        if float(f"{number:.{i}f}") != 0:
                #return this precision string
                return f"{number:.{i}f}"
    #no matches found, return max precision string
    return f"{number:.{max_precision}f}"
