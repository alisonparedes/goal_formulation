'''
Created on Aug 18, 2016

@author: lenovo
'''

import operator #TODO: What does this do exactly?
import sys
from Canvas import Line

#class State(object): #TODO: Why an object? I want a function to be able to take a human-readable representation of the game state and return its value
#    '''
#    '''
    
def __init__(self, simstate): 
    '''
    Takes a visual representation of the current state and parses it into an internal representation. (Yes, I've been thinking about knowledge representation lately) 
    '''
    
    
def parse(simstate): #Could recursively split first and rest and send rest to the parse function. Function returns a list of units and their coordinates.
    '''
    '''
    
    state = {}
    
    y=0
    x=0
    
    for cell in simstate:
    
        if cell in 'HB*!':
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
    
    if action:
        simstate += 'Action:{0}\n'.format(action)
    
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
    
    simstate += 'Reward:{0}\n'.format(reward(state)) 
    
    return simstate

def reward(state): #TODO: I really want to make this a higher-order function
    ordered = xref(state)
    reward = 0
    reward += is_at_base(ordered)
    reward += are_fighting(ordered)
    return reward
    
def is_at_base(ordered):
    if '*' in ordered: 
        return 100
    return 0

def xref(state):
    units = {}
    for cell in state.items():
        units[cell[1]] = cell[0]
    return units

def are_fighting(ordered):
    if '!' in ordered:
        return -10
    return 0
        
if __name__ == '__main__': #Read in a simulated state and write it out
    
    import fileinput
    
    simstate = ''
    for line in fileinput.input():
        simstate += line
    print(write(parse(simstate)))
    