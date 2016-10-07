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

def write(state, h, w): #TODO: Move to agent module.
    '''
    A state is a dictionary of positions and objects, keyed on position. Use to write the agent's perspective. 
    '''
    grid = to_grid(state, h, w)
    printable = write_grid(grid) #TODO: Modify agent's new knowledge function. Cell's known to contain None are different from unknown cells.   
    return printable

def interleaved(known, world):
    height=len(world[0])
    width=len(world)
    known_grid = to_grid(known, height, width) 
    printable = ''
    for y in range(height):
        for x in range(width):
            cell = world[x][y]
            if cell:
                printable += cell
            else:
                printable += '-'
        printable += ' '
        for x in range(width): #TODO: Should agent know boundaries of teh world? World's transition model does. What about imagined view of the world?
            cell = known_grid[x][y] 
            if cell:
                printable += cell
            else:
                printable += '?' #TODO: Modify agent's new knowledge function. Cell's known to contain None are different from unknown cells.
        printable += '\n'
    return printable
    
def write_grid(state):
    '''
    A state is a 2D array
    '''
    width=len(state)
    height=len(state[0])
    simstate = ''
    for y in range(height):
        for x in range(width):
            cell = state[x][y]
            if cell:
                simstate += cell
            else:
                simstate += '-'
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

def applicable_actions1(s, h, w): #TODO: How shall I distinguish top-level planner's actions from hindsight planner's action model?
    actions=[]
    units='' #TODO: Maybe use this when adding Defender's moves
    for coordinate, unit in s.iteritems():
        x=coordinate[0] 
        y=coordinate[1]
        if unit in 'H*$':#TODO: Or D
            if y-1 >= 0:
                actions.append('N')
            if y+1 < h: #Internal representation of coordinate system puts origin in upper left corner of map
                actions.append('S')
            if x+1 < w:
                actions.append('E')            
            if x-1 >= 0: #Assuming left most cell in problem is 0
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
    
def new_coordinate(coordinate, action):
    '''
    Returns a new coordinate for an action, could be negative!
    ''' 
    x=coordinate[0]
    y=coordinate[1]
    if action == 'N':
        y += -1;
    elif action == 'S':
        y += 1;
    elif action == 'E':
        x += 1;
    elif action == 'W': 
        x += -1;
    return (x,y)

'''def get_coordiante(s, world):
    return (0,0) #TODO: Get coordinate(s)? of a unit in the world. Overkill?'''


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
    
def to_grid(s, w, h): 
    '''
    Takes a dictionary and returns a 2D representation
    '''
    grid = []
    for i in range(w): #TODO: I don't need i.
        grid.append([None]*h) #Meh
    for coordinate, unit in s.iteritems():
        x=coordinate[0]
        y=coordinate[1]
        grid[x][y]=unit
    return grid

def to_dict(w):
    '''
    Takes a grid and returns a dictionary (an interim solution until the rest of problem's functions deal with grids
    '''
    state={}
    x=0
    for col in w:
        y=0
        for cell in col:
            if cell:
                state[(x,y)]=cell
            y+=1
        x+=1
    return state
                
def transition1(s, action, world): #TODO: I really want to put these top level action and transitions into a separate problem module. S isn't really a state. Fix this!
    '''
    Takes a state, an action, and a world (grid)  and returns a new world. Transition may not always be possible.
    '''
    #TODO: Separate functions maybe?
    from_coordinate=get_coordinate(s)
    from_x = from_coordinate[0]
    from_y = from_coordinate[1]
    unit = world[from_x][from_y] #TODO: I hope this is a copy!
    world[from_x][from_y]=leaving(unit) #TODO: May need to replace old location to get performance stats in the interim
    to_coordinate = new_coordinate(from_coordinate, action)
    to_x = to_coordinate[0]
    to_y = to_coordinate[1] 
    #TODO: Try the move and if it fails return?
    cell=world[to_x][to_y]
    world[to_x][to_y]=arriving('H', cell) #TODO: Moves may not always work
    return world #TODO: What about returning the new state? 

def get_coordinate(s):
    for coordinate, cell in s.iteritems():
        if cell in 'H*$':
            return coordinate
    return None

def get_state(w): #TODO: For now, to keep reasoning about the problem here, parse the Harvester's current state out of the world.
    state={}
    x=0
    for col in w:
        y=0
        for cell in col:
            if cell in 'H*$':
                state[(x,y)]=cell
            y+=1
        x+=1
    return state

def leaving(unit):
    if unit=='H':
        return None
    if unit=='*':
        return 'B'
    if unit=='$':
        return 'F'
    return None
    
def arriving(unit, cell):
    if cell=='B':
        return '*'
    if cell=='F':
        return '$'
    #if cell=='@':
    #    return 'H'
    return unit
        
if __name__ == '__main__': #Read in a simulated state and write it out
    dict={(1, 0): 'H', (3, 1): 'B'}
    to_grid(dict,4,4)
    w=[[None, None, None, None], ['H', 'B', None, None], [None, 'B', None, None], [None, 'B', None, None]]
    print(w)
    w = transition1((1,0),'S',w)
    print(w)
    w = transition1((1,1),'E',w)
    print(w)
    w = transition1((2,1),'N',w)
    print(w)    
    w = transition1((2,0),'W',w)
    print(w) 
    print applicable_actions1(dict, 4, 4)   
    