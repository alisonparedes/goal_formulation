'''
Created on Aug 18, 2016

@author: lenovo
'''


from collections import namedtuple
from copy import deepcopy
import dijkstra
import random


def to_state(grid_dict, reward=0, t=0, future_food=[], distances={}):
    State = namedtuple('State', ['grid', 'reward', 't', 'future_food', 'distances'])
    return State(grid_dict, reward, t, future_food, distances)

    
def parse(simstate):
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


def applicable_actions(state, problem):
    harvester = find_harvester(state.grid)
    actions = unit_actions(harvester.coordinate, state.grid, problem)
    return actions


def unit_actions(coordinate, grid, problem):
    actions = []
    x = coordinate[0]
    y = coordinate[1]
    if y-1 >= 0 and ((x, y-1) not in grid or grid[(x, y-1)] != '#'):
        actions.append('N')
    if y+1 < problem.y and ((x, y+1) not in grid or grid[(x, y+1)] != '#'):
        actions.append('S')
    if x+1 < problem.x and ((x+1, y) not in grid or grid[(x+1, y)] != '#'):
        actions.append('E')
    if x-1 >= 0 and ((x-1, y) not in grid or grid[(x-1, y)] != '#'):
        actions.append('W')
    return actions


def to_grid(s, problem_spec):
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


def transition(state, action, harvester_world):
    new_from_cell, new_to_cell = move(state, action)
    if new_to_cell[1] and new_to_cell[1] in '#':  # Sometimes the action available in the beilef state is not really available
        observation = to_observation({(new_to_cell.coordinate): '#'})
        return state, observation
    new_grid = deepcopy(state.grid)
    new_grid[new_from_cell[0]] = new_from_cell[1]
    new_grid[new_to_cell[0]] = new_to_cell[1]
    new_grid, remaining_food = replace_food(new_grid, state.future_food, harvester_world.max_food)
    new_reward = reward(new_grid) + state.reward
    observations = to_observation({new_from_cell[0]: new_from_cell[1], new_to_cell[0]: new_to_cell[1]}, reward=new_reward)
    new_state = to_state(new_grid, reward=new_reward, future_food=remaining_food)
    return new_state, observations


def move(state, action):
    harvester = find_harvester(state.grid)
    new_from_symbol = leaving_symbol(harvester.cell)
    new_to_coordinate = to_coordinate(harvester.coordinate, action)
    to_symbol = state.grid.get(new_to_coordinate, None)
    new_to_symbol = arriving(harvester.cell, to_symbol)
    return (harvester.coordinate, new_from_symbol), (new_to_coordinate, new_to_symbol)


def to_observation(dict, reward=0):
    Observation = namedtuple("Observation", ["dict", "reward"])
    return Observation(dict, reward)


def to_coordinate(coordinate, action):
    x=coordinate[0]
    y=coordinate[1]
    if action == 'N':
        y += -1
    elif action == 'S':
        y += 1
    elif action == 'E':
        x += 1
    elif action == 'W':
        x += -1
    return x, y


def leaving_symbol(from_symbol):
    if from_symbol in 'H$':
        return None
    if from_symbol in '*b':
        return 'B'
    return None


def replace_food(grid, future_food, max_food):
    if find_harvester(grid).cell != '$':
        return grid
    remaining_food = deepcopy(future_food)
    new_grid = deepcopy(grid)
    while (count_food(new_grid) < max_food):
        new_grid = add_food(new_grid, remaining_food.pop())
    return new_grid, remaining_food


def add_food(grid, coordinate):
    new_grid = deepcopy(grid)
    if coordinate in new_grid:
        if new_grid[coordinate] in 'H$':
            new_grid[coordinate] = '$'
    else:
        new_grid[coordinate] = 'F'
    return new_grid


def reward(grid):
    new_reward=0
    base = find_base(grid)
    if base[1] == '*':
        new_reward += 50
    return new_reward


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


def chance_of_food(state, problem):
    distribution = no_chance(state)
    total_probability = 0.0
    probability = 1.0/ (problem.x * problem.y - len(distribution))
    for x in range(0, problem.x):
        for y in range(0, problem.y):
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


def find_harvester(grid):
    for coordinate, cell in grid.iteritems():
        if cell and cell in 'bH*$':
            return coordinate, cell
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


def sample(belief_state, food_dist, dimensions):
    complete_grid = sample_food(food_dist, belief_state.grid, dimensions.max_food)
    future_food = sample_future_food(food_dist, n=100)
    to_base = distance_to_base(complete_grid, dimensions)
    food_distances = add_distance_to_food(complete_grid, to_base, dimensions)
    all_distances = add_distance_to_future(complete_grid, food_distances, future_food, dimensions )
    return to_state(complete_grid, belief_state.reward, distances=all_distances)


def sample_food(food_dist, grid, max_food):
    new_grid = deepcopy(grid)
    while count_food(new_grid) < max_food:
        x = sample_cell(food_dist)
        new_grid = add_food(new_grid, x)
    return new_grid


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


def add_food(grid, sample):
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
    if not unit_a:
        return unit_b
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
        probability = cell[0]
        cummulative += probability
    return cell


def distance_to_base(grid, problem):
    new_distance = []
    base = find_base(grid)
    new_distance.append((base, dijkstra.dijkstra(base[0], grid, problem)))
    return new_distance


def add_distance_to_food(grid, distance, problem):
    new_distance = deepcopy(distance)
    food = find_food(grid)
    for f in food:
        new_distance.append((f, dijkstra.dijkstra(f[0], grid, problem)))
    return new_distance


def add_distance_to_future(grid, distance, future_food, problem):
    new_distance = deepcopy(distance)
    for f in future_food:
        new_distance.append((f, dijkstra.dijkstra(f, grid, problem)))
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


def to_problem(x, y, max_food=0):
    Problem = namedtuple("Problem", ["x", "y", "max_food"])
    return Problem(x, y, max_food)


if __name__ == '__main__':
    pass
    
