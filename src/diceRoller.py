import discord

import numpy as np
from datetime import datetime


# custom dice roller using numpy and datetime (in the ms range) for rng
def roll(message):

    # finds the second spacebar in message and remove anything behind it.
    a = message.find(" ")
    if a != -1:
        message = message[:a]


    ## from here on, the message only has the first term (eg: 5d20)
    ## break message up into before d and after d
    
    # finds the d ;)
    ind = message.find("d")
    if ind == -1:
        # if there is no d
        return discord.Embed(title = "Error!", description = "The syntax is `=r ndx` where `n` is the number of dice, and `x` is the number of faces on each die", color = 0x880000)
    #print(ind)

    
    ## split message up relative to the index
    if ind == 0:
        # if no dice amount specified, assume 1
        numOfDice = 1
    else:
        # otherwise pull it from message content
        numOfDice = int(message[:ind])
    # grabs the numbers before the d
    if len(message[ind+1:]) == 0:
        return discord.Embed(title = "Error!", description = "Please specify number of dice faces.\nEg: `5d20` rolls five 20-sided dice.", color = 0x880000)
    diceFaces = int(message[ind+1:])
    
    # numbers after the d
    #if diceFaces == "":
    #    print(diceFaces)

    
    ## make sure the user is not off the rails
    if numOfDice > 120:
        # who needs more than 120 dice?
        return discord.Embed(title = "Too many dice!\nPlease don't hurt yourself. (The limit is 120 dice)", color = 0x880000)
    
    if diceFaces > 120:
        # at this point it's a sphere
        return discord.Embed(title = "Too many faces!\nYou couldn't tell which face was up. (The limit 120 faces)", color = 0x880000)
    

    ## okay let's actually generate some random numbers
    dtn = str(datetime.now())
    # get current system date/time as a string
    dtn = dtn[-5:]
    # get rid of the first bit. We only use the tiny ms or smaller
    if dtn.find(".") != -1:
        dtn = dtn.replace(":", "0")
        dtn = dtn.replace(".", "0")
    # In the rare case that it finds a : or ., replace with a zero
    # dtn is now a very random number.
    
    rng = np.random.default_rng(int(dtn))
    # take in time based seed as int for np's rng
    diceRolls = rng.integers(1, diceFaces, numOfDice, int, True)
    drTotal = sum(diceRolls)

    ## of course it's not that simple. Gotta format the numbers nicely
    diceRolls = str(diceRolls)
    # convert it into a string to format things
    diceRolls = diceRolls[1:]
    diceRolls = diceRolls[:-1]
    # gets rid of square brackets
    if diceRolls.find(" ") == 0:
        # if the first char is a spacebar, get rid of it!
        diceRolls = diceRolls[1:]


    diceRolls = ", ".join(diceRolls.split())
    # gets rid of excess whitespaces! split method splits string into string array.
    # join joins it back together using only one whitespace between.=
    # it also adds a comma between each number
    # the list is now 1, 2, 20, 3, etc
    
    ## alright now let's make the embed 
    desc = "Rolled: " + str(numOfDice) + "d" + str(diceFaces)
    desc = desc + "\n**[" + diceRolls + "]** \nTotal: " + str(drTotal)
    # description definition
    reply = discord.Embed(title = "Dice roll", description = desc, color = 0x888888)
    return reply
