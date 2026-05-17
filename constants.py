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


___SHOW_AMOUNT_OF_CAULDRON_POSSIBILITIES___ = 100

