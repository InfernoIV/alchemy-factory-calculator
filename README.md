# alchemy-factory-calculator
Calculator for alchemy factory

Usage:
python3 main.py "<resource>" <amount>

Only resource is mandatory
Amount gives a specific amount, if omitted: gives the original (time scaled) recipe

e.g.
python3 main.py plank 5
python3 main.py coke
python3 main.py "copper powder"


TODO list:
5. consolidate recipes (in printing) 
    e.g. total output is 60, but 20 and 30 is needed: only 1 device should be used and not 2
    Hard to do due to back and forth calculations -> do a total need calculation and then use the original recipe to check for amount of devices