'''
Created on Aug 18, 2016

@author: lenovo
'''

import operator #TODO: What does this do?
import sys

#class State(object): #TODO: Why an object? I want a function to be able to take a human-readable representation of the game state and return its value
#    '''
#    '''
    
def __init__(self, simstate): #TODO: Need a list of goals (high-level actions?)
    '''
    Takes a visual representation of the current state and parses it into an internal representation, a dictionary of positions and objects.
    '''
    
def parse(simstate): #Could recursively split first and rest and send rest to the parse function. Function returns a list of units and their coordinates.
    '''
    '''  
    state = {}   
    y=0
    x=0    
    for cell in simstate:   
        if cell in 'HBF$*!':
            state[(x,y)]=cell       
        elif cell=='\n':
            y += 1
            x=-1 #Hmm...        
        x += 1    
    return state

def write(state, action=None):
    '''
    A state is a dictionary of positions and objects, keyed on position.
    '''
    ordered = sorted(state.items(), key=operator.itemgetter(0)) #TODO: 
    simstate = ''
    cell = (-1, 0)
    for object in ordered:
        location = object[0]
        name = object[1] #TODO: This name isn't quite accurate since objects could be obstacles 
        simstate += '\n' * (location[1] - cell[1])
        y = location[1]
        simstate += ' ' * (location[0] - cell[0] - 1)
        simstate += name
        x = location[0]
    simstate += '\n'
    return simstate

def c(state): #TODO: I really want to make this a higher-order function
    return 0 #TODO: For now you get nothing special for any particular configuration of the world

def applicable_actions(state): #TODO: Units (or combinations of units, e.g. fleet) takes actions so state model needs to provide quick access to units' positions.  Although if world is small enough iterating through dictionary of positions may not be that big of a problem, .e.g one harvester and one base.
    '''
    Returns an iterable list of actions applicable in the given state.
    '''
    #TODO: What is definitive list of actions? HB and HF only for now.
    HB = 1 #move harvester to base
    HF = 2 #move harvester to food
    return [HB,HF]

def transition(state, action):
    '''
    Returns the next state (s') from the current state (s) given an action.
    '''
    #TODO: For example, if actions HTOB, look up harvester's current position and base's position then remove harvester from current position and add to base's position.
    if action == 1: #HB
        return hb(state)
    if action == 2: #HF
        return hf(state)
    return state 

def hb(state):
    '''
    Problem specific
    '''
    next_state = {}
    base = None
    for coordinate, unit in state.iteritems():
        if unit == 'H':
            pass
        elif unit == 'B':
            base = coordinate
            pass
        else:
            next_state[coordinate]=unit
    next_state[base]='*'
    return next_state

def hf(state):
    '''
    Problem specific
    '''
    next_state = {}
    food = None
    for coordinate, unit in state.iteritems():
        if unit == 'H':
            pass
        elif unit == 'F':
            food = coordinate
            pass
        else:
            next_state[coordinate]=unit
    next_state[food]='$'
    return next_state
        
if __name__ == '__main__': #Read in a simulated state and write it out
    pass
    