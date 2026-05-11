import sys


#base pokemon object, containing information of the pokemon
class recipe(object):

    #initial values
    name = ""
    output = ""
    amount = 0
    time = 0
    device = ""
    inputs = []
    

    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        #recipe-name, output-amount, output-resource, time, device, input-1-amount, input-1-resource,

        #print("dict: ", dict)

        #guard clauses
        flag_guarded = False
        
        #check the number
        if dict["recipe-name"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing recipe-name")
        
        #check the number
        if dict["output-amount"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing output-amount")

        #check the number
        if dict["output-resource"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing output-resource")

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

        #check the number
        if dict["input-1-amount"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing input-1-amount")

        #check the number
        if dict["input-1-resource"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            print("Missing input-1-resource")
                  
        #if there is a guard
        if flag_guarded == True:
            #stop the script
            sys.exit(f"dict: {dict}")  

        #data is correct, start conversion to object 
        self.name = dict["recipe-name"]
        self.output = dict["output-resource"]
        self.amount = int(dict["output-amount"])
        self.time = int(dict["time"])
        self.device = dict["device"]
        self.inputs = []
        
        #self.factor = 60/self.time

        #for the possible inputs
        for i in range(1, 9): 
            #get resource
            resource = dict[f"input-{i}-resource"]
            #get amount
            amount = dict[f"input-{i}-amount"]
            #if resource is empty
            if resource == None or resource == "":
                #no more resources: stop
                break
            else:
                #add information to list
                self.inputs.append({resource:amount})



    #function that will print when converted to str
    def __repr__(self):
        #string to return
        string = f"{self.amount} {self.output} requires {self.time}s on a {self.device} with the following inputs: {self.inputs}"
        #for each attribute
        #for attr, value in self.__dict__.items():
            #add to return string
        #    string += f"'{attr}': '{value}', "
        #remove string while removing the last ', ' 
        #return string[:-2]
        return string