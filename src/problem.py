'''
Created on Aug 18, 2016

@author: lenovo
'''


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

def write(state, problem_spec): #TODO: Move to agent module.
    '''
    A state is a dictionary of positions and objects, keyed on position. Use to write the agent's perspective. 
    '''
    grid = to_grid(state, problem_spec)
    printable = write_grid(grid) #TODO: Modify agent's new knowledge function. Cell's known to contain None are different from unknown cells.   
    return printable

def interleaved(known, world, problem_spec):
    height=len(world[0])
    width=len(world)
    known_grid = to_grid(known, problem_spec)
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

def empty(cell):
    if cell:
        return cell
    else:
        return '-'
    
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

def applicable_actions(belief_state, problem_spec): #TODO: Use a problem definition instead of dimensions
    actions=[]
    w=problem_spec[0]
    h=problem_spec[1]
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



def reset(state_dict, problem_distribution_arr, n=1):  #TODO: Consider getting size of world from somewhere else, a problem structure maybe?
    '''
    Expects a state of the world. It doesn't need to be a completely known state of the world (I think) but because I expect
    this function to be used by the simulator which is omniscient and not the agent which has limited knolwedge, spawn must be able to
    deal with a complete state, all n of its attributes.
    
    State must be a dictionary. Right now there may be two representations of states floating around, dictionaries and 2D grids. There are functions that transform
    one format to the other but which functions prefer which versions? I don't want to worry about this but ... sigh. 
    '''
    #state_dict = to_dict(state)
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
    
def to_grid(s, problem_spec):
    '''
    Takes a dictionary and returns a 2D representation
    '''
    grid = []
    w=problem_spec[0]
    h=problem_spec[1]
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
                
def transition(state, action, problem_spec):
    '''
    Transition is used by both search to imagine the next state and the simulator to take an action. It could operate on a belief state
    or a complete state. 
    '''
    #TODO: Separate functions maybe? But I don't want to revert to using dictionaries.
    state_grid = to_grid(state, problem_spec) #TODO: Get dimensions from problem spec
    from_coordinate=get_coordinate(state) #TODO: Currently moves harvester only. Why not get this from world?
    from_x = from_coordinate[0]
    from_y = from_coordinate[1]
    unit = state_grid[from_x][from_y] #TODO: I hope this is a copy!
    leaving_unit = leaving(unit)
    state_grid[from_x][from_y]= leaving_unit#TODO: May need to replace old location to get performance stats in the interim
    to_coordinate = new_coordinate(from_coordinate, action)
    to_x = to_coordinate[0]
    to_y = to_coordinate[1] 
    #TODO: Try the move and if it fails return?
    cell=state_grid[to_x][to_y]
    arriving_unit = arriving('H', cell) #TODO: Moves may not always work
    state_grid[to_x][to_y]=arriving_unit #TODO: Moves may not always work
    state_dict = to_dict(state_grid)
    observation_dict={}
    observation_dict[(from_x, from_y)]= empty(leaving_unit) #TODO: Name this function something better
    observation_dict[(to_x, to_y)]= arriving_unit
    Transition = namedtuple('Transition',['state_dict','observation_dict'])
    new_state = Transition(state_dict=state_dict, observation_dict=observation_dict)
    return new_state #TODO: What about returning new observations to the agent?

def problem_distribution(belief_state_dict, problem_spec): #TODO: Problem spec is width and height of a single test problem right now
    problem_distribution_arr = []
    for coordinate, unit in belief_state_dict.iteritems():
        problem_distribution_arr.append((0.0, coordinate, unit)) #There is no chance an attribute of the belief state could be different, for now
    #TODO: Make a function for this
    total_probability=0.0
    for x in range(0, problem_spec[0]):
        for y in range(0, problem_spec[1]):
            if (x, y) not in belief_state_dict:
                probability = 0.1
                problem_distribution_arr.append((probability, (x, y), 'F')) 
                total_probability += probability
    problem_distribution_arr.append((1 - total_probability, None))        
    return problem_distribution_arr


def reset_distribution(state_dict, problem_spec): #TODO: Oh my god stop doing this :)
    problem_distribution_arr = []
    inventory={}
    #To allow this program to run forever, there should always be a chance that new food will spawn somewhere at least
    for coordinate, unit in state_dict.iteritems():
        if unit in '0f':
            problem_distribution_arr.append((0.1,coordinate,'F')) #Chance to reset food
        if unit in 'Bb*$F!':
            problem_distribution_arr.append((0.0,coordinate,'B')) #New food can't spawn
            # where food already is available, on a base
        if unit not in inventory:
            inventory[unit]=1
        else:
            inventory[unit]+=1
    total_probability=0.0
    MAX_FOOD = 1 #TODO: Need to update action descriptions for multiple food
    if 'F' in inventory and inventory['F'] < MAX_FOOD:
        for x in range(0, problem_spec[0]):
            for y in range(0, problem_spec[1]):
                if (x, y) not in state_dict:
                    probability = 0.1
                    problem_distribution_arr.append((probability, (x, y), 'F'))
                    total_probability += probability
    problem_distribution_arr.append((1 - total_probability, None)) 
    return problem_distribution_arr

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
    if unit in '*!':
        return 'b'
    if unit in '0$':
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
    
