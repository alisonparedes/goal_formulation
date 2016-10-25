'''
Created on Aug 18, 2016

@author: lenovo
'''

import operator #TODO: What does this do?
import sys
from collections import namedtuple
import world

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
                printable += '?' #TODO: Modify agent's new knowledge function. Cells known to contain None are different from unknown cells.
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

def applicable_actions(belief_state, h, w): #TODO: Use a problem definition instead of dimensions
    actions=[]
    units='' #TODO: Maybe use this when adding Defender's moves
    for coordinate, unit in belief_state.iteritems():
        x=coordinate[0] 
        y=coordinate[1]
        if unit in 'H*$0!':#TODO: Or D
            if y-1 >= 0:
                actions.append('N')
            if y+1 < h: #Internal representation of coordinate system puts origin in upper left corner of map
                actions.append('S')
            if x+1 < w:
                actions.append('E')            
            if x-1 >= 0: #Assuming left most cell in problem is 0
                actions.append('W')#TODO: Eventually both harvester and defender should be able to move: units+=unit
                
    return actions



def spawn(state, n=1):  #TODO: Consider getting size of world from somewhere else, a problem structure maybe?
    '''
    Spawn expects a state of the world. It doesn't need to be a completely known state of the world (I think) but because I expect
    this function to be used by the simulator which is omniscient and not the agent which has limited knolwedge, spawn must be able to
    deal with a complete state, all n of its attributes.
    
    State must be a dictionary. Right now there may be two representations of states floating around, dictionaries and 2D grids. There are functions that transform
    one format to the other but which functions prefer which versions? I don't want to worry about this but ... sigh. 
    '''
    problem_distribution_arr = [(0.5,(0,0),'F'),(0.5,None)]
    state_dict = to_dict(state)
    new_state = world.sample(problem_distribution_arr, state_dict, n)  #TODO: Need to be able to seed the sample for debugging
    return new_state
    
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
                
def transition(state, action):
    '''
    Transition is used by both search to imagine the next state and the simulator to take an action. It could operate on a belief state
    or a complete state. 
    '''
    #TODO: Separate functions maybe? But I don't want to revert to using dictionaries.
    state_grid = to_grid(state, 4, 2) #TODO: Get dimensions from problem spec
    print(state_grid)
    from_coordinate=get_coordinate(state) #TODO: Currently moves harvester only. Why not get this from world?
    from_x = from_coordinate[0]
    from_y = from_coordinate[1]
    unit = state_grid[from_x][from_y] #TODO: I hope this is a copy!
    state_grid[from_x][from_y]=leaving(unit) #TODO: May need to replace old location to get performance stats in the interim
    to_coordinate = new_coordinate(from_coordinate, action)
    to_x = to_coordinate[0]
    to_y = to_coordinate[1] 
    #TODO: Try the move and if it fails return?
    cell=state_grid[to_x][to_y]
    state_grid[to_x][to_y]=arriving('H', cell) #TODO: Moves may not always work
    state_dict = to_dict(state_grid)
    return state_dict #TODO: What about returning new observations to the agent?

def get_coordinate(state):
    for coordinate, cell in state.iteritems():
        if cell in 'H*$!0':
            return coordinate
    return None

def get_state(w): #TODO: For now, to keep reasoning about the problem here, parse the Harvester's current state out of the world.
    state={}
    x=0
    for col in w:
        y=0
        for cell in col:
            if cell in 'H*$!0':
                state[(x,y)]=cell
            y+=1
        x+=1
    return state

def leaving(unit):
    if unit=='H':
        return None
    if unit=='*':
        return 'b'
    if unit=='$':
        return 'f'
    return None
    
def arriving(unit, cell):
    if cell=='B':
        return '*'
    if cell=='b':
        return '!'
    if cell=='F':
        return '$'
    if cell=='f':
        return '0'
    #if cell=='@':
    #    return 'H'
    return unit
        
if __name__ == '__main__': #Read in a simulated state and write it out
    pass
    
