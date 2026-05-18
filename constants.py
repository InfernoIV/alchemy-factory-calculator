#constants to be imported by other scripts
___CSV_RECIPES____ = "data/recipes.csv"
___CSV_RECIPES_CAULDRON____ = "data/recipes_cauldron.csv"
___CSV_CAULDRON____ = "data/cauldron.csv"


___PREFERRED_RECIPES___ = [
    "coke",
    "charcoal",
    "iron ingot",
    "coal",
    "copper ingot",
    "iron sand",
    "sand",
    "stone",
    "plank",
    "crude shard",
    "adamant",
    "shattered crystal",
    "copper powder and impure copper powder",

    # to check what is best for gold dust
    # "pure gold dust",
    #"gold ingot",
    #"gold dust",
    #"pure gold dust 2",
    
    "gold ingot 2",
    
    #either:
    #"ruby",
    #"sapphire",
    #"emerald",
    
    #or:
    #"stone and coal",
]

#list of preferred resources, and their fertilizer cost @ 60 / min
___PREFERRED_RESOURCES___ = {
    "flax":0.01, "flax fiber":0.01,
    "sage":0.01, "sage powder":0.01,
    "redcurrant":0.04,
    "lavender":0.65,
    "chamomile":0.22, "chamomile powder":0.22,
    "gentian":1.8, "gentian powder":1.8, "gentian nectar":1.8, #1/2 due to split output, but 2 needed for 60 output 
    "world tree leaf":18, 
}


#key = resource, value = fertilizer cost, heat cost
#TODO: verify calculation for clay
___PREFERRED_RESOURCES_EXTENDED___ = {
    #fertilizer: 0.67, heat: 235, score: 184.5, inputs: flax, flax fiber, lavender
    "impure copper powder":0.67, 

    #fertilizer: 0.45, heat: 131, score: 114.0, inputs: chamomile, chamomile powder, flax
    "turquoise":1.09,

    #fertilizer: 2.24, heat: 537, score: 331.5, inputs: chamomile, chamomile, gentian
    #fertilizer: 2.24, heat: 537, score: 344.5, inputs: chamomile, chamomile, gentian nectar
    "copper powder":2.24,

    #fertilizer: 1.82, heat: 699, score: 404.5, inputs: flax, flax fiber, gentian
    #fertilizer: 1.82, heat: 699, score: 424.5, inputs: flax, flax fiber, gentian nectar
    "malachite":1.82,

    #fertilizer: 0.24, heat: 65.6, score: 59.5, inputs: chamomile, flax, flax fiber
    "salt":0.24, 

    #fertilizer: 1.09, heat: 403, score: 292.0, inputs: chamomile, chamomile powder, lavender
    "gloom spores":1.09, 

    #fertilizer: 0.06, heat: 16.6, score: 17.5, inputs: flax, redcurrant, sage powder
    #or fertilizer: 0.06, heat: 16.6, score: 18.0, inputs: flax fiber, redcurrant, sage powder
    "clay":0.06, 

    #fertilizer: 0.73, heat: 190, score: 132.6, inputs: lavender, redcurrant, redcurrant
    "black powder":0.73, 

    #fertilizer: 3.61, heat: 1538, score: 823.0, inputs: gentian, gentian nectar, sage
    "unstable catalyst":3.61,

    #fertilizer: 3.61, heat: 2040, score: 853.0, inputs: gentian nectar, gentian powder, sage
    "vitality essence":3.61,

    #fertilizer: 0.88, heat: 343, score: 237.0, inputs: chamomile, flax, lavender
    "sulfur":0.88,

    #fertilizer: 2.03, heat: 896, score: 488.0, inputs: chamomile, gentian powder, sage
    #fertilizer: 2.03, heat: 896, score: 478.0, inputs: chamomile, gentian nectar, sage
    "crude shard":2.03,

    #fertilizer: 7.89, heat: 7647, score: 1796.0, inputs: impure copper powder, unstable catalyst, vitality essence
    "crude silver powder":7.89,

    #fertilizer: 5.40, heat: 3244, score: 1250.0, inputs: gentian, gentian nectar, gentian powder
    "topaz":5.40,

    #fertilizer: 4.25, heat: 2448, score: 1000.0, inputs: gentian, gentian nectar, lavender
    "broken shard":4.25,

    #fertilizer: 12.17, heat: 10315, score: 2170.0, inputs: crude silver powder, impure copper powder, unstable catalyst
    "dull shard":12.17,

    #fertilizer: 19.81, heat: 8155, score: 2902.0, inputs: flax, gentian, world tree leaf
    #fertilizer: 19.81, heat: 8155, score: 2922.0, inputs: flax, gentian nectar, world tree leaf
    "impure silver powder":19.81,
}


___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___ = 100

