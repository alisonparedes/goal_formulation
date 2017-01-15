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
        if cell in 'HbBF$*#':
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
    height=problem_spec[1]
    width=problem_spec[0]
    known_grid = to_grid(known, problem_spec)
    world_grid = to_grid(world, problem_spec)
    printable = ''
    for y in range(height):
        for x in range(width):
            cell = world_grid[x][y]
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
    for coordinate, unit in belief_state.grid.iteritems():
        if unit in 'H*$b':#TODO: Or Defender?
            actions = unit_actions(coordinate, belief_state, problem_spec)
    return actions

'''
Given a coordinate returns a list of actions that may be taken from that coordinate in the given state.
'''


def unit_actions(coordinate, belief_state, problem_spec):

    actions = []

    w = problem_spec[0]
    h = problem_spec[1]

    x = coordinate[0]
    y = coordinate[1]

    if y-1 >= 0 and ((x, y-1) not in belief_state.grid or belief_state.grid[(x, y-1)] != '#'):
        actions.append('N')
    if y+1 < h and ((x, y+1) not in belief_state.grid or belief_state.grid[(x, y+1)] != '#'): # Internal representation of coordinate system puts origin in upper left corner of map
        actions.append('S')
    if x+1 < w and ((x+1, y) not in belief_state.grid or belief_state.grid[(x+1, y)] != '#'):
        actions.append('E')
    if x-1 >= 0 and ((x-1, y) not in belief_state.grid or belief_state.grid[(x-1, y)] != '#'): # Assuming left most cell in problem is 0
        actions.append('W')

    return actions


def grow(state, coordinate, State):

    grid = state.grid

    if coordinate in grid:
        if grid[coordinate] in 'H$':
            grid[coordinate] = '$'
    else:
        grid[coordinate] = 'F'

    return State(grid, state.reward, state.t)
    
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

'''
Transition expects a state and an action and returns a state and an observation. The problem spec helps determine how
the state changes.

A state is made up of three features: ...

Action determine which of the units that an agent may control may attempt move and to where, although the move may not
resolve as expected; units may not get as far as they had hoped, moving 0 to n - m.

Encountering food changes if the agent has food or not and causes new food to grow somewhere else.

'''


'''
Transition is used to simulate next step.
'''


def transition(state, action, problem_spec, State, here=None):

    Observation = namedtuple('Observation',['observation_dict', 'reward'])
    observation_dict={}
    Transition = namedtuple('Transition',['state','observations'])

    state_grid = to_grid(state.grid, problem_spec)

    from_coordinate = find_harvester(state.grid)[0]
    from_x = from_coordinate[0]
    from_y = from_coordinate[1]

    unit = state_grid[from_x][from_y]
    leaving_unit = leaving(unit)
    state_grid[from_x][from_y] = leaving_unit

    to_coordinate = new_coordinate(from_coordinate, action)
    to_x = to_coordinate[0]
    to_y = to_coordinate[1]

    cell = state_grid[to_x][to_y]

    if cell and cell in '#':
        observation_dict[(to_x, to_y)]='#'
        return Transition(state, observations=Observation(observation_dict, reward=0))

    arriving_unit = arriving(unit, cell)

    state_grid[to_x][to_y]=arriving_unit

    grid = to_dict(state_grid)

    observation_dict[(from_x, from_y)] = empty(leaving_unit) #TODO: Name this function something better
    observation_dict[(to_x, to_y)] = arriving_unit

    new_reward = reward(State(grid=grid, reward=state.reward, t=0))

    observations = Observation(observation_dict, reward=new_reward)
    new_state = State(grid=grid, reward=new_reward, t=0)

    maxfood = 2
    i = 0
    while (here and i < len(here) and arriving_unit in '$' and world.count_food(grid) < maxfood):
        new_state = grow(new_state, here[i], State)
        i+=1

    new_state_and_observations = Transition(new_state, observations=observations)

    return new_state_and_observations

def reward(state):
    reward=0
    base = find_base(state.grid)
    if base[1] == '*':
        reward += 50
    return reward

def clear_visited(state_grid):
    cleared = state_grid
    x=0
    for col in state_grid:
        y=0
        for cell in col:
            if cell == '-':
                cleared[x][y] = None
            y += 1
        x += 1
    return cleared


'''

'''

def chance_of_food(state, problem_spec):

    distribution = []

    food = 0
    for coordinate, unit in state.grid.iteritems():
        if unit in 'F':
            food += 1
        elif unit in 'b*B#': # Food cannot grow in cell occupied by the base or an obstacle
            distribution.append((0.0, coordinate))

    total_probability = 0.0

    probability = 1.0/ (problem_spec[0] * problem_spec[1] - len(distribution))
    for x in range(0,problem_spec[0]):
        for y in range(0,problem_spec[1]):
            if (x, y) not in state.grid or state.grid[(x, y)] not in 'b*B#':
                distribution.append((probability, (x, y), 'F'))
                total_probability += probability

    distribution.append((1 - total_probability, None))
    return distribution


def find_harvester(state):
    for coordinate, cell in state.iteritems():
        if cell and cell in 'bH*$':
            return (coordinate, cell)
    return None


def leaving(from_symbol):
    if from_symbol in 'H$':
        return None
    if from_symbol in '*b':
        return 'B'
    return None

    
def arriving(from_symbol, to_symbol):
    if from_symbol == '$' and to_symbol == 'B':  # A harvester carrying food
        return '*' # Gets a reward
    if from_symbol in '$H*b' and to_symbol == 'F':
        return '$'
    if from_symbol in 'H' and to_symbol == 'B':
        return 'b' # Does not get a reward
    if from_symbol in 'b*' and to_symbol and to_symbol in 'b*B':
        return 'b'
    if from_symbol in 'b*':
        return 'H'
    return from_symbol

def find_base(grid):
    for coordinate, unit in grid.iteritems():
        if unit and unit in 'Bb*':
            return coordinate, unit
    return None

def find_food(grid):
    food = []
    for coordinate, unit in grid.iteritems():
        if unit in 'F':
            food.append((coordinate, unit))
    return food
        
if __name__ == '__main__': #Read in a simulated state and write it out
    pass
    
