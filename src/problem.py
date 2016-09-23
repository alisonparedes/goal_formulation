'''
Created on Aug 18, 2016

@author: lenovo
'''

import operator #TODO: What does this do?
import sys
from collections import namedtuple

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
        if cell in 'HBF$*!@':
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

def applicable_actions(s): #TODO: Units (or combinations of units, e.g. fleet) takes actions so state model needs to provide quick access to units' positions.  Although if world is small enough iterating through dictionary of positions may not be that big of a problem, .e.g one harvester and one base.
    '''
    Returns an iterable list of actions applicable in the given state.
    '''
    #TODO: What is definitive list of actions? For now harvester should always have exactly two applicable actions.
    HB = 1 #move harvester to base
    HF = 2 #move harvester to food
    HS = 3 #move harvester somewhere else
    actions=[]
    units=''
    for coordinate, unit in s.state.iteritems():
        if unit in 'HBF$*@':
            units+=unit
    if ('H' in units or '$' in units) and 'B' in units:
        actions.append(HB)
    if ('H' in units or '*' in units) and 'F' in units:
        actions.append(HF)
    if ('*' in units or '$' in units) and '@' in units:
        actions.append(HS)
    return actions
    #return [1,2]

def top_applicable_actions(s, h, w): #TODO: How shall I distinguish top-level planner's actions from hindsight planner's action model?
    actions=[]
    units='' #TODO: Maybe use this when adding Defender's moves
    for coordinate, unit in s.state.iteritems():
        x=coordinate[0] #TODO: How much performance do I loose using named tuples?
        y=coordinate[1]
        if unit in 'H':#TODO: Or D
            if y-1 >= 0:
                actions.append('N')
            elif y+1 < h: #Internal representation of coordinate system puts origin in upper left corner of map
                actions.append('S')
            elif x-1 >= 0:
                actions.append('E')            
            elif x+1 < w: #Assuming left most cell in problem is 0
                actions.append('W')#TODO: Eventually both harvester and defender should be able to move: units+=unit
    return actions

def transition(s, action, State, Simulated): #TODO: Assumes action is valid
    '''
    Returns the next state (s') and its value(?) from the current state (s) given an action. 
    '''
    if action == 1: #HB
        simulated=hb(s.state, Simulated) #TODO: I'm not sure I like passing data structures around but it seems like it should belong to functional programming
    elif action == 2: #HF
        simulated=hf(s.state, Simulated)
    elif action == 3: #HS
        simulated=hs(s.state, Simulated)
    resources=simulated.resources
    new_reward=s.reward + reward(s.state) - resources 
    return State(simulated.state, new_reward) #
    #return s

def top_transition(s, action, State): #TODO: I really want to put these top level action and transitions into a separate problem module
    N = -1
    S = +1
    E = -1
    W = +1 
    #TODO: Move units
    next_state = {}
    for coordinate, unit in s.iteritems():
        if unit == 'H': #TODO: Add *$. What about E?
            x = coordinate[0]
            y = coordinate[1]
            if action == 'N':
                next_state[(x,y+N)]=unit #TODO: +N feels overengineered but not very well
        else:
            next_state[coordinate]=unit 
    #TODO: Update reward
    return State(next_state,)

def reward(state):
    reward=0
    for coordinate, unit in state.iteritems(): #TODO: How much is this slowing my BFS down?
        if unit == '$':
            reward+=50
        elif unit == '*':
            reward+=100

    return reward

def hb(state, Simulated): 
    '''
    Simulate moving harvester to base
    '''
    next_state = {}
    for coordinate, unit in state.iteritems():
        if unit == 'H':
            next_state[coordinate]='@' #Start
        elif unit == '$': #TODO: Top level planners may need to use the same symbols
            next_state[coordinate]='F' #Food
        elif unit == 'B':
            next_state[coordinate]='*'
        else:
            next_state[coordinate]=unit #TODO: Too much iterating!
    return Simulated(next_state,resources=-1)
    #return (state,-1)

def hf(state, Simulated):
    '''
    Simulate moving harvester to food
    '''
    next_state = {}
    for coordinate, unit in state.iteritems():
        if unit == 'H':
            next_state[coordinate]='@' #Start
        elif unit == 'F':
            next_state[coordinate]='$' #Food
        elif unit == '*':
            next_state[coordinate]='B' #Base
        else:
            next_state[coordinate]=unit
    return Simulated(next_state,resources=-1)
    #return (state,-1)


def hs(state, Simulated):
    '''
    Simulate harvester somewhere else
    '''
    next_state = {}
    for coordinate, unit in state.iteritems():
        if unit == '$':
            next_state[coordinate]='F'
        elif unit == '*':
            next_state[coordinate]='B'
        elif unit == '@':
            next_state[coordinate]='H'
        else:
            next_state[coordinate]=unit
    return Simulated(next_state,resources=-1)
    #return (state,-1)
        
if __name__ == '__main__': #Read in a simulated state and write it out
    pass
    