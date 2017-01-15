'''
Created on Oct 25, 2016

@author: lenovo
'''
import problem
from copy import deepcopy

def applicable_actions(s): #TODO: Units (or combinations of units, e.g. fleet) takes actions so state model needs to provide quick access to units' positions.  Although if world is small enough iterating through dictionary of positions may not be that big of a problem, .e.g one harvester and one base.
    '''
    Returns an iterable list of actions applicable in the given state.
    '''
    actions=[]
    units=''
    food_coordinates=[]
    for coordinate, unit in s.grid.iteritems():
        if unit and unit in 'F':
            food_coordinates.append(coordinate)
        if unit and unit in 'HbBF$*':
            units += unit
    if ('H' in units or '$' in units ) and ('B' in units):
        actions.append('HB')
    if ('H' in units or '*' in units or 'b' in units) and ('F' in units):
        for food_coordinate in food_coordinates:
            actions.append('HF' + '_' + str(food_coordinate[0]) + '_' + str(food_coordinate[1]))
    '''if ('*' in units or '$' in units or '!' in units) and '@' in units:
        actions.append('HS')'''

    return actions
    #return [1,2]
    
def transition(state, action_and_coordinate, distances, State):
    '''
    Returns the next state (s') and its value(?) from the current state (s) given an action. 
    '''
    action = action_and_coordinate.split('_')[0]
    next_state = None
    if action == 'HB':
        next_state = hb(state, distances, State)
    elif action == 'HF':
        coordinate = (int(action_and_coordinate.split('_')[1]), int(action_and_coordinate.split('_')[2]))
        next_state = hf(state, coordinate, distances, State)
    return next_state
    #return s

def hb(state, distances, State):
    '''
    Simulate moving harvester to base
    '''
    new_grid = deepcopy(state.grid)

    harvester = problem.find_harvester(state.grid)
    base = problem.find_base(state.grid)

    new_grid[base[0]] = problem.arriving(harvester[1], base[1])
    new_grid[harvester[0]] = problem.leaving(harvester[1])

    resources = find_distances_to_base(distances)[1][harvester[0]][1] # Second index in distance dictionary is distance; first is policy
    new_reward = state.reward
    next_state = State(new_grid,new_reward)
    new_reward += problem.reward(next_state) - resources
    return State(new_grid, new_reward)

def find_distances_to_base(distances):
    for d in distances:
        if d[0][1] in 'Bb*':
            return d
    return None


def find_distances_to_food(distances, food):
    for d in distances:
        if d[0][0] == food:
            return d
    return None

def distance(from_coordinate, to_coordinate):
    from_x=float(from_coordinate[0])
    from_y=float(from_coordinate[1])
    to_x=float(to_coordinate[0])
    to_y=float(to_coordinate[1])
    distance=abs(from_x - to_x) + abs(from_y - to_y)
    return distance * 1


'''
Simulate moving harvester to food
'''
def hf(state, food_coordinate, distances, State):

    new_grid = deepcopy(state.grid)

    harvester = problem.find_harvester(state.grid)
    food = (food_coordinate, 'F')

    new_grid[food_coordinate] = problem.arriving(harvester[1], food[1])
    new_grid[harvester[0]] = problem.leaving(harvester[1])

    distance = find_distances_to_food(distances, food_coordinate)
    resources = distance[1][harvester[0]][1] # Second index in distance dictionary is distance; first is policy

    new_reward = state.reward
    next_state = State(new_grid, new_reward)
    new_reward += problem.reward(next_state) - resources
    return State(new_grid, new_reward)


if __name__ == '__main__':
    pass