import sys
import math

#base pokemon object, containing information of the pokemon
class recipe(object):

    #initial values
    name = ""
    output = ""
    amount = 0
    time = 0
    device_name = ""
    device_amount = 1
    inputs = {}
    factor_time = 1
    factor_amount = 1
    child_recipes = {}
    cauldron_recipe = False

    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict, cauldron_recipe):
        #recipe-name, output-amount, output-resource, time, device, input-1-amount, input-1-resource,
        #save if this is a cauldron recipe
        self.cauldron_recipe = cauldron_recipe
        #print("dict: ", dict)

        #guard clauses
        flag_guarded = False
        
        

        #check the output
        if dict["output-resource"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing output-resource")

       

        #check the number
        if dict["input-1-resource"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing input-1-resource")        

        #if cauldron recipe          
        if self.cauldron_recipe:
            #check if amount is filled in
            if dict["amount"] == "":
                #set flag
                flag_guarded = True 
                #missing number
                print("Missing amount")
        else:
            #check the name
            if dict["recipe-name"] == "":
                #set flag
                flag_guarded = True 
                #missing number
                print("Missing recipe-name")

            #check if amount is filled in
            if dict["output-amount"] == "":
                #set flag
                flag_guarded = True 
                #missing number
                print("Missing output-amount")

            #check the number
            if dict["time"] == "":
                #set flag
                flag_guarded = True 
                #missing number
                print("Missing time")

            #check the number
            if dict["device"] == "":
                #set flag
                flag_guarded = True 
                #missing number
                print("Missing device")

        #if there is a guard
        if flag_guarded == True:
            #stop the script
            sys.exit(f"dict: {dict}")  



        #data is correct, start conversion to object 
        self.output = dict["output-resource"].lower()
        self.inputs = {}  

        #specifics to cauldron recipe
        if self.cauldron_recipe:
            self.name = f"{self.output} (cauldron)"
            self.time = 60
            self.factor_time = 1
            self.device_name = "cauldron"
            self.amount = int(dict["amount"])

            #for the possible inputs
            for i in range(1, 4): 
                #get resource
                resource = dict[f"input-{i}-resource"]
                
                #add information to list
                self.inputs[resource] = self.amount 

        #specifics to normal recipe
        else:
            self.name = dict["recipe-name"].lower()
            #set device name
            self.device_name = dict["device"].lower()
            #normalize to 60s
            self.time = int(dict["time"])
            #calculate time factor (this also applies to input)
            self.factor_time = 60/self.time
            #re-set the time to 60 s
            self.time = 60
            #get amount
            amount = int(dict["output-amount"])          
            #apply time factor to amount
            self.amount = self.factor_time * amount

            #for the possible inputs
            for i in range(1, 9): 
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
                    amount = self.factor_time*int(dict[f"input-{i}-amount"])
                    #add information to list
                    self.inputs[resource] = amount



    #function that will print when converted to str
    def __repr__(self):
        inputs = ""
        for resource, amount in self.inputs.items():
            if inputs != "":
                inputs += ", "
            inputs += f"{amount:.2f} {resource}"

        #string to return
        string = f"recipe '{self.name}' requires {self.amount:.2f} {self.output} using {self.device_amount} {self.device_name}"
        
        if inputs != "":
            string += f" with inputs: {inputs}"

        #return the string
        return string
    


    def adjust_amount(self, amount):
        #calculate the factor
        self.factor_amount = amount / self.amount
        #set the amount to the needed amount
        self.amount = amount

        #print(f"before: {self.device_amount}, factor: {self.factor_amount}")
        #calculate the needed devices
        self.device_amount =  math.ceil(self.device_amount * self.factor_amount)
        #print(f"after: {self.device_amount}")
        
        #calculate the inputs
        for resource in self.inputs.keys():
            self.inputs[resource] *= self.factor_amount