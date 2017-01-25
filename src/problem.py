'''
Created on Aug 18, 2016

@author: lenovo
'''


from collections import namedtuple
from copy import deepcopy
import dijkstra
import random


def to_state(grid_dict, x=0, y=0, max_food=0, reward=0, t=0, future_food=[], distances={}):
    State = namedtuple('State', ['grid', 'x', 'y', 'max_food', 'reward', 't', 'future_food', 'distances'])
    return State(grid_dict, x, y, max_food, reward, t, future_food, distances)

    
def parse(simstate): #Could recursively split first and rest and send rest to the parse function. Function returns a list of units and their coordinates.
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
        for x in range(width): #
            cell = known_grid[x][y] 
            if cell:
                printable += cell
            else:
                printable += '?'
        printable += '\n'
    return printable


def empty(cell):
    if cell:
        return cell
    else:
        return '-'


def applicable_actions(state):
    harvester = find_harvester(state)
    return unit_actions(harvester.coordinate, state)


def unit_actions(coordinate, state):
    actions = []
    x = coordinate[0]
    y = coordinate[1]
    if y-1 >= 0 and ((x, y-1) not in state.grid or state.grid[(x, y-1)] != '#'):
        actions.append('N')
    if y+1 < state.y and ((x, y+1) not in state.grid or state.grid[(x, y+1)] != '#'):
        actions.append('S')
    if x+1 < state.x and ((x+1, y) not in state.grid or state.grid[(x+1, y)] != '#'):
        actions.append('E')
    if x-1 >= 0 and ((x-1, y) not in state.grid or state.grid[(x-1, y)] != '#'):
        actions.append('W')
    return actions


def grow(state, coordinate, State):
    grid = deepcopy(state.grid)
    if coordinate in grid:
        if grid[coordinate] in 'H$':
            grid[coordinate] = '$'
    else:
        grid[coordinate] = 'F'
    return State(grid, state.reward, state.t, deepcopy(state.future_food))


def new_coordinate(coordinate, action):
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


def to_observation(grid_dict, reward=0):
    Observation = namedtuple('Observation',['cell_dict', 'reward'])
    return Observation(grid_dict, reward)


def transition(state, action):
    observation_dict={}
    Transition = namedtuple('Transition',['state','observations'])

    state_grid = to_grid(state.grid)

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
        return Transition(state, observations=to_observation(observation_dict, reward=0))

    arriving_unit = arriving(unit, cell)

    state_grid[to_x][to_y]=arriving_unit

    grid = to_dict(state_grid)

    observation_dict[(from_x, from_y)] = empty(leaving_unit) #TODO: Name this function something better
    observation_dict[(to_x, to_y)] = arriving_unit

    new_reward = reward(to_state(grid=grid, reward=state.reward, t=0, future_food=state.future_food))

    observations = to_observation(observation_dict, reward=new_reward)
    new_state = to_state(grid=grid, reward=new_reward, t=0, future_food=state.future_food)

    while (len(here) > 0 and arriving_unit in '$' and count_food(grid) < maxfood):
        new_state = grow(new_state, here.pop(), State)

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


def chance_of_food(state):
    distribution = no_chance(state)
    total_probability = 0.0
    probability = 1.0/ (state.x * state.y - len(distribution))
    for x in range(0,state.x):
        for y in range(0, state.y):
            if (x, y) not in state.grid or state.grid[(x, y)] not in 'b*B#':
                distribution.append((probability, (x, y), 'F'))
                total_probability += probability
    distribution.append((1 - total_probability, None))
    return distribution


def no_chance(state):
    distribution = []
    for coordinate, unit in state.grid.iteritems():
        if unit in 'b*B#':  # Food cannot grow in cell occupied by the base or an obstacle
            distribution.append((0.0, coordinate))
    return distribution


def find_harvester(state):
    for coordinate, cell in state.grid.iteritems():
        if cell and cell in 'bH*$':
            return to_unit(coordinate, cell)
    return None


def to_unit(coordinate, cell):
    Unit = namedtuple("Unit", ["coordinate", "cell"])
    return Unit(coordinate, cell)


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


def sample(belief_state, food_dist):
    complete_state = sample_food(food_dist, belief_state)
    future_state = sample_future_food(food_dist, belief_state, n=100)
    distance_to_base = distance_to_base(future_state)
    all_distances = add_distance_to_food(distance_to_base, future_state)
    return to_state(complete_state.grid, belief_state.reward, t=0, future_food=future_food, distances=distance)

def sample_food(food_dist, state):
    new_grid = deepcopy(state.grid)
    while count_food(new_grid) < state.max_food:
        x = sample_cell(food_dist)
        new_grid = add_food(new_grid, x)
    new_state = replace_grid(new_grid, state)
    return new_state


def replace_grid(state, new_grid):
    new_state = to_state(new_grid,
                state.x,
                state.y,
                state.max_food,
                state.reward,
                state.t,
                deepcopy(state.future_food),
                deepcopy(state.distances))
    return new_state


def sample_future_food(food_dist, n=1):
    food_sequence = []
    while n > 0:
        sampled_food = sample_cell(food_dist)[1]  #TODO: Use the same list of random numbers as the simulator
        food_sequence.append(sampled_food)
        n -= 1
    return food_sequence


def count_food(grid):
    food = 0
    for coordinate, unit in grid.iteritems():
        if unit == 'F':
            food += 1
    return food


def add_food(grid, sample): #Modifies state in place
    new_grid = deepcopy(grid)
    coordinate = sample[1]
    if coordinate:
        unit = sample[2]
        if coordinate in grid:
            new_unit = merge(new_grid[coordinate], unit)
            new_grid[coordinate] = new_unit
        else:
            new_grid[coordinate] = unit
    return new_grid


def merge(unit_a, unit_b):
    if unit_a in 'b$*H' and unit_b in 'F':
        return '$'
    if unit_a in '$' and unit_b in 'B':
        return '*'
    if unit_a in 'H' and unit_b in 'B':
        return 'b'
    if unit_a in 'b*':
        return 'H'
    return unit_b


def sample_cell(problem_distribution_arr):
    p = random.random()
    cummulative = 0
    i=-1
    while cummulative < p:
        i += 1
        cell = problem_distribution_arr[i]
        probability=cell[0]
        cummulative += probability
    return cell


def distance_to_base(state):
    new_distance = []
    base = find_base(state.grid)
    new_distance.append((base, dijkstra.dijkstra(base[0], state)))
    return new_distance


def add_distance_to_food(distance, state):
    new_distance = deepcopy(distance)
    food = find_food(state.grid)
    for f in food:
        new_distance.append((f, dijkstra.dijkstra(f[0], state)))
    return new_distance


def add_distance_to_future(distance, state):
    new_distance = deepcopy(distance)
    for f in state.future_food:
        new_distance.append((f, dijkstra.dijkstra(f, state )))
    return new_distance


def adjacent_coordinate(coordinate, action):
    x = y = 0
    if action == 'N':
        y = -1
    elif action == 'S':
        y = 1
    elif action == 'E':
        x = 1
    elif action == 'W':
        x = -1
    next_x = coordinate[0] + x
    next_y = coordinate[1] + y
    return next_x, next_y

        
if __name__ == '__main__':
    pass
    
