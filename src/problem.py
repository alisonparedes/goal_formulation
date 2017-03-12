'''
Created on Aug 18, 2016

@author: lenovo
'''
import random
import copy

from collections import namedtuple
from copy import deepcopy  # I am not sure if copy would have been sufficient
import dijkstra


def to_problem(x, y, max_food=0, known=False):
    Problem = namedtuple("Problem", ["x", "y", "max_food", "known"])
    return Problem(x, y, max_food, known)


def to_state(grid_dict, reward=0, future_food=[], distances={}):
    State = namedtuple('State', ['grid', 'reward', 'future_food', 'distances'])
    return State(grid_dict, reward, future_food, distances)


def to_observation(dict, reward=0):
    Observation = namedtuple("Observation", ["dict", "reward"])
    return Observation(dict, reward)


def parse(simstate):
    """Input"""
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


def interleaved(world, known, problem_spec):
    """Output"""
    height = problem_spec[1]
    width = problem_spec[0]
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
        for x in range(width):
            cell = known_grid[x][y] 
            if cell:
                printable += cell
            else:
                printable += '?'
        printable += '\n'
    return printable


def print_grid(world, problem_spec):
    height = problem_spec[1]
    width = problem_spec[0]
    world_grid = to_grid(world, problem_spec)
    printable = ''
    for y in range(height):
        for x in range(width):
            cell = world_grid[x][y]
            if cell:
                printable += cell
            else:
                printable += '-'
        printable += '\n'
    return printable


def to_grid(s, problem_spec):
    grid = []
    w = problem_spec[0]
    h = problem_spec[1]
    for _ in range(w):
        grid.append([None]*h) #Meh
    for coordinate, unit in s.iteritems():
        x = coordinate[0]
        y = coordinate[1]
        if not unit:
            unit = '-'
        grid[x][y] = unit
    return grid


def applicable_actions(state, problem):
    """Summarizes all actions available for all units."""
    harvester_coordinate, _ = find_harvester(state.grid)
    actions = unit_actions(harvester_coordinate, state.grid, problem)
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


def transition(state, action, harvester_world):
    """Does a lot of stuff!"""
    # rint("Transition from:\n")
    # print(print_grid(state.grid, harvester_world))
    new_from_cell, new_to_cell = move(state, action, harvester_world)

    if new_to_cell[1] and new_to_cell[1] in '#':  # Sometimes the action available in the beilef state is not really available
        observation = to_observation({(new_to_cell[0]): '#'})
        return state, observation

    new_grid = deepcopy(state.grid)
    new_grid[new_from_cell[0]] = new_from_cell[1]
    new_grid[new_to_cell[0]] = new_to_cell[1]

    #if new_from_cell[1] and new_from_cell[1] in '*$':
    if found_food(state.grid, new_grid):
        new_grid = del_explored_cell(new_grid)

    # new_grid, remaining_food, new_food = replace_food(new_grid, state.future_food, harvester_world.max_food)

    new_reward = reward(new_grid) + state.reward

    obs_from_sym = new_from_cell[1]
    if not obs_from_sym:
        obs_from_sym = '-'
    observations = to_observation({new_from_cell[0]: obs_from_sym, new_to_cell[0]: new_to_cell[1]}, reward=new_reward)

    remaining_food = state.future_food
    while count_food(new_grid) < harvester_world.max_food:
        new_food, remaining_food = sample_replacement_food(new_grid, state.future_food)
        new_grid[new_food] = 'F'

        if harvester_world.known and new_food:
            observations.dict[new_food] = 'F'

    # new_state = to_state(new_grid, reward=new_reward, future_food=remaining_food, distances=state.distances)
    new_state = to_state(new_grid, reward=new_reward, future_food=remaining_food, distances=state.distances)
    # print("Transition to:\n")
    # print(print_grid(new_state.grid, harvester_world))
    return new_state, observations


def move(state, action, harvester_world):
    harvester_coordinate, harvester_symbol = find_harvester(state.grid)
    new_from_symbol = leaving_symbol(harvester_symbol)
    new_to_coordinate = to_coordinate(harvester_coordinate, action, harvester_world)
    to_symbol = state.grid.get(new_to_coordinate, None)
    if to_symbol and to_symbol in '#':
        return (harvester_coordinate, harvester_symbol), (new_to_coordinate, to_symbol)
    new_to_symbol = arriving(harvester_symbol, to_symbol)
    return (harvester_coordinate, new_from_symbol), (new_to_coordinate, new_to_symbol)


def to_coordinate(coordinate, action, harvester_world):
    x = coordinate[0]
    y = coordinate[1]
    if action == 'N' and y - 1 >= 0:
        y += -1
    elif action == 'S' and y + 1 < harvester_world.y:
        y += 1
    elif action == 'E' and x + 1 < harvester_world.x:
        x += 1
    elif action == 'W' and x - 1 >= 0:
        x += -1
    return x, y


def leaving_symbol(from_symbol):
    if from_symbol in 'H$':
        return None
    if from_symbol in '*b':
        return 'B'
    return None


def replace_food(grid, future_food, max_food):
    _, harvester_symbol = find_harvester(grid)
    if harvester_symbol != '$':
        return grid, future_food, None
    remaining_food = deepcopy(future_food)
    new_grid = deepcopy(grid)
    new_food = None
    while count_food(new_grid) < max_food:
        try_coordinate = remaining_food.pop()
        new_grid, new_food = add_food(new_grid, try_coordinate)
        remaining_food.insert(0, try_coordinate)

    return new_grid, remaining_food, new_food


def add_food(grid, coordinate):
    new_grid = deepcopy(grid)
    if coordinate in new_grid:
        if not new_grid[coordinate] or new_grid[coordinate] in 'H$':
            return grid, None  # new_grid[coordinate] = '$'
    else:
        new_grid[coordinate] = 'F'
    return new_grid, coordinate


def reward(grid, time=0):
    new_reward = 0
    _, base_symbol = find_base(grid)
    if base_symbol == '*':
        new_reward += 50 * pow(0.95, time)
    return new_reward


def find_harvester(grid):
    for coordinate, cell in grid.iteritems():
        if cell and cell in 'bH*$':
            return coordinate, cell
    return None

    
def arriving(from_symbol, to_symbol):
    if from_symbol == '$' and to_symbol == 'B':  # A harvester carrying food
        return '*' # Gets a reward
    if from_symbol in 'b*$H' and to_symbol == 'F':
        return '$'
    if from_symbol in 'H' and to_symbol == 'B':
        return 'b'  # Does not get a reward
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
        if unit and unit in 'F':
            food.append((coordinate, unit))
    return food


def chance_of_food(state, problem):
    """Food cannot grow in cells that have been explored e.g. unit == None"""
    distribution = no_chance(state)
    total_probability = 0.0
    probability = 1.0 / (problem.x * problem.y - len(distribution))
    for x in range(0, problem.x):
        for y in range(0, problem.y):
            if (x, y) not in state.grid or not state.grid[(x, y)] or (state.grid[(x, y)] and state.grid[(x, y)] not in '#*Bb'):
                distribution.append((probability, (x, y), 'F'))
                total_probability += probability
    distribution.append((1 - total_probability, None))
    return distribution


def no_chance(state):
    """Food cannot grow in cells that have been explored, e.g. unit == None"""
    distribution = []
    for coordinate, unit in state.grid.iteritems():
        if not unit or unit in 'b*B#':
            distribution.append((0.0, coordinate))
    return distribution


def sample(belief_state, dimensions):
    """Constructs a world from a belief state"""
    complete_grid = sample_max_food(belief_state.grid, dimensions)
    if dimensions.known:
        future_food = belief_state.future_food
    else:
        future_food = sample_n_future_food(dimensions, 100000)
    distances = all_distances(complete_grid, dimensions)
    # to_base = distance_to_base(complete_grid, dimensions)
    # food_distances = add_distance_to_food(complete_grid, to_base, dimensions)
    # all_distances = add_distance_to_future(complete_grid, food_distances, future_food, dimensions)
    return to_state(complete_grid, belief_state.reward, distances=distances, future_food=future_food)


# def sample_food(food_dist, grid, max_food):
#     new_grid = deepcopy(grid)
#     print(food_dist)
#     while count_food(new_grid) < max_food:
#         cell = sample_cell(food_dist)
#         if cell and cell[1] not in grid:  # Food cannot grow where agent has already explored
#             new_grid = add_food(new_grid, cell[1])
#     return new_grid


# def sample_future_food(food_dist, n=1):
#     food_sequence = []
#     while n > 0:
#         sampled_food = sample_cell(food_dist)[1]  #TODO: Use the same list of random numbers as the simulator
#         if sampled_food:  # There is a small chance that we sampled no food
#             food_sequence.append(sampled_food)
#             n -= 1
#     return food_sequence


def count_food(grid):
    food = 0
    for coordinate, unit in grid.iteritems():
        if unit == 'F':
            food += 1
    return food


# def add_food(grid, coordinate):
#     new_grid = deepcopy(grid)
#     if coordinate:
#         if coordinate in grid:
#             new_unit = merge(new_grid[coordinate], 'F')
#             new_grid[coordinate] = new_unit
#         else:
#             new_grid[coordinate] = 'F'
#     return new_grid


def merge(unit_a, unit_b):
    if not unit_a:
        return unit_b
    if unit_a in '-':
        return unit_b
    if unit_a in '$H' and unit_b in 'F':
        return '$'
    if unit_a in '*' and unit_b in 'F':
        return '*'
    if unit_a in 'b' and unit_b in 'F':
        return 'b'
    if unit_a in '$' and unit_b in 'B':
        return '*'
    if unit_a in 'H' and unit_b in 'B':
        return 'b'
    if unit_a in 'b*':
        return 'H'
    return unit_b


# def sample_cell(problem_distribution_arr):
#     p = random.random()
#     cummulative = 0
#     i =- 1
#     while cummulative < p:
#         i += 1
#         cell = problem_distribution_arr[i]
#         probability = cell[0]
#         cummulative += probability
#     return cell


def distance_to_base(grid, problem):
    """Distances can be used to look up the cost of an action"""
    new_distance = []
    base = find_base(grid)
    new_distance.append((base, dijkstra.dijkstra(base[0], grid, problem)))
    return new_distance


def all_distances(grid, problem):
    distances = []
    for x in range(problem.x):
        for y in range(problem.y):
            if (x, y) not in grid or not grid[(x, y)] or grid[(x, y)] not in '#':
                distances.append(((x, y), dijkstra.dijkstra((x, y), grid, problem)))
    return distances


def add_distance_to_food(grid, distance, problem):
    new_distance = deepcopy(distance)
    food = find_food(grid)
    for f in food:
        new_distance.append((f, dijkstra.dijkstra(f[0], grid, problem)))
    return new_distance


def add_distance_to_future(grid, distance, future_food, problem):
    new_distance = deepcopy(distance)
    for f in future_food:
        if not find_distances_to_food(new_distance, f):
            new_distance.append(((f, 'F'), dijkstra.dijkstra(f, grid, problem)))
    return new_distance


def find_distances_to_base(distances):
    for d in distances:
        if d[0][1] in 'Bb*':
            return d
    return None


def find_distances_to_food(distances, food):
    for d in distances:
        if d[0] == food:
            return d
    return None


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


def found_food(old_belief, cell_dict):
    for coordinate, cell in cell_dict.iteritems():
        if cell and cell in '$':
            for _, belief_cell in old_belief.iteritems():
                if belief_cell and belief_cell in '$':
                    return False
            return True


def del_explored_cell(grid):
    explored = list_explored_cell(grid)
    new_grid = deepcopy(grid)
    for coordinate, _ in explored.iteritems():
        del new_grid[coordinate]
    return new_grid


def list_explored_cell(grid):
    explored = {}
    for coordinate, cell in grid.iteritems():
        if cell and cell in '-':
            explored[coordinate] = cell
    return explored


def sample_cell(width, height):
    sampled_x = random.randint(0, width - 1)
    sampled_y = random.randint(0, height - 1)
    return sampled_x, sampled_y


def try_food(grid, coordinate):
    if coordinate not in grid:
        return coordinate
    if grid[coordinate] and grid[coordinate] in 'Bb*#H$-':
        return None
    return coordinate


def sample_max_food(grid, dimensions):
    #print(grid)
    new_grid = deepcopy(grid)
    while count_food(new_grid) < dimensions.max_food:
        #print(try_coordinate)
        try_coordinate = sample_cell(dimensions.x, dimensions.y)
        coordinate = try_food(grid, try_coordinate)
        if coordinate:
            new_grid[coordinate] = 'F'
    return new_grid


def sample_replacement_food(grid, future_food):
    remaining_food = copy.copy(future_food)
    while True:
        try_x = remaining_food.pop()
        try_y = remaining_food.pop()
        # print(try_x, try_y)
        remaining_food.insert(0, try_x)
        remaining_food.insert(0, try_y)
        coordinate = try_food(grid, (try_x, try_y))
        if coordinate:
            return coordinate, remaining_food

def try_future_food(grid, coordinate):
    if coordinate not in grid:
        return coordinate
    if grid[coordinate] in 'Bb*#':
        return None
    if grid[coordinate] in 'H$':
        return coordinate


def sample_n_future_food(harvester_world, n=1):
    food_sequence = []
    for _ in range(n):
        food_sequence.append(random.randint(0, harvester_world.x - 1))
    return food_sequence


if __name__ == '__main__':
    # grid = {}
    # harvester_world = to_problem(2, 2)
    # d = all_distances(grid, harvester_world)
    # print(d)

    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("action")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = to_problem(x, y, int(args.max_food))
    complete_grid = sample_max_food(initial_state.grid, harvester_world)

    # To replace food distribution in sampling the following need to work
    # complete_grid = sample_food(food_dist, belief_state.grid, dimensions.max_food)
    # future_food = sample_future_food(food_dist, n=100)
    distances = all_distances(complete_grid, harvester_world)
    future_food = sample_n_future_food(harvester_world, 100)
    new_state = to_state(complete_grid, initial_state.reward, distances=distances, future_food=future_food)
    # food_dist = chance_of_food(initial_state, harvester_world)
    initial_state = sample(initial_state, harvester_world)
    next_state, observations = transition(initial_state, args.action, harvester_world)
    # belief_state = agent.update_belief(initial_state, observations)
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    # print print_grid(initial_state.grid, harvester_world)
    # print print_grid(complete_grid, harvester_world)
    print "action: {0}".format(args.action)
    # print "reward: {0}".format(next_state.reward)
    print(interleaved(initial_state.grid, next_state.grid, harvester_world))
    print(observations)
    # random.seed(0)

    
