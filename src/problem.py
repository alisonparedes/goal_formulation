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


def to_state(base, harvester, food=None, obstacle=None, defender=None, enemy=None, explored=None, has_food=False, reward=0, future_food=[], distances={}):
    State = namedtuple('State', ['base_dict',
                                 'harvester_dict',
                                 'food_dict',
                                 'obstacle_dict',
                                 'defender_dict',
                                 'enemy_dict',
                                 'explored_dict',
                                 'has_food',
                                 'reward',
                                 'future_food',
                                 'distances'])
    if not explored:
        explored = {}
    return State(base, harvester, food, obstacle, defender, enemy, explored, has_food, reward, future_food, distances)


def to_observation(dict, reward=0):
    Observation = namedtuple("Observation", ["dict", "reward"])
    return Observation(dict, reward)


def parse(simstate):
    base = {}
    harvester = {}
    food = {}
    obstacle = {}
    defender = {}
    enemy = {}
    has_food = False
    y = 0
    x = 0
    for cell in simstate:

        if cell == 'b':
            harvester[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == 'H':
            harvester[(x, y)] = cell

        elif cell == 'B':
            base[(x, y)] = cell

        elif cell == 'F':
            food[(x, y)] = cell

        elif cell == '$':
            harvester[(x, y)] = cell
            food[(x, y)] = cell
            has_food = True

        elif cell == '*':
            harvester[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == '#':
            obstacle[(x, y)] = cell

        elif cell == 'D':
            defender[(x, y)] = cell

        elif cell == 'd':
            harvester[(x, y)] = cell
            defender[(x, y)] = cell

        elif cell == 'E':
            enemy[(x, y)] = cell

        elif cell == '\n':
            y += 1
            x =- 1 #Hmm...
        x += 1    
    return base, harvester, food, obstacle, defender, enemy, has_food


def interleaved(world, known, problem_spec):
    """Output"""
    height = problem_spec[1]
    width = problem_spec[0]
    #known_grid = to_grid(known, problem_spec)
    #world_grid = to_grid(world, problem_spec)
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


def print_grid(state, world):

    state_grid = [[" " for _ in range(world.y)] for _ in range(world.x)]

    for explored, _ in state.explored_dict.iteritems():
        explored_x, explored_y = explored
        state_grid[explored_x][explored_y] = '-'

    for obstacle, _ in state.obstacle_dict.iteritems():
        obstacle_x, obstacle_y = obstacle
        state_grid[obstacle_x][obstacle_y] = '#'

    for food, _ in state.food_dict.iteritems():
        food_x, food_y = food
        state_grid[food_x][food_y] = 'F'

    for base, _ in state.base_dict.iteritems():
        base_x, base_y = base
        state_grid[base_x][base_y] = 'B'

    harvester, _ = state.harvester_dict.iteritems().next()
    harvester_x, harvester_y = harvester
    if harvester in state.base_dict:
        if state.has_food:
            state_grid[harvester_x][harvester_y] = '*'
        else:
            state_grid[harvester_x][harvester_y] = 'b'
    elif harvester in state.food_dict:
        state_grid[harvester_x][harvester_y] = '$'
    else:
        state_grid[harvester_x][harvester_y] = 'H'

    defender_item = next(state.defender_dict.iteritems(), None)
    if defender_item:
        defender, _ = defender_item
        defender_x, defender_y = defender
        if defender in state.harvester_dict:
            state_grid[defender_x][defender_y] = 'd'
        if defender in state.base_dict:
            state_grid[defender_x][defender_y] = 'b'
        elif defender in state.food_dict:
            state_grid[defender_x][defender_y] = 'd'
        else:
            state_grid[defender_x][defender_y] = 'D'

    enemy_item = next(state.enemy_dict.iteritems(), None)
    if enemy_item:
        enemy, _ = enemy_item
        enemy_x, enemy_y = enemy
        if enemy in state.harvester_dict:
            state_grid[enemy_x][enemy_y] = 'e'
        elif enemy in state.base_dict:
            state_grid[enemy_x][enemy_y] = 'b'
        elif enemy in state.food_dict:
            state_grid[enemy_x][enemy_y] = 'e'
        elif enemy in state.defender_dict:
            state_grid[enemy_x][enemy_y] = 'x'
        else:
            state_grid[enemy_x][enemy_y] = 'E'

    printable = ''
    for y in range(world.y):
        for x in range(world.x):
            printable += state_grid[x][y]
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


def unit_actions(coordinate, state, problem):
    actions = []
    x = coordinate[0]
    y = coordinate[1]
    if y-1 >= 0 and ((x, y-1) not in state.obstacle_dict):
        actions.append('N')
        actions.append('ND')
    if y+1 < problem.y and ((x, y+1) not in state.obstacle_dict):
        actions.append('S')
        actions.append('SD')
    if x+1 < problem.x and ((x+1, y) not in state.obstacle_dict):
        actions.append('E')
        actions.append('ED')
    if x-1 >= 0 and ((x-1, y) not in state.obstacle_dict):
        actions.append('W')
        actions.append('WD')
    return actions


def transition(state, action, world):

    move_harvester_in_direction = action[0]
    move_defender_too = False
    if len(action) > 1 and action[1] == 'D':
        move_defender_too = True
    harvester, _ = state.harvester_dict.iteritems().next()
    new_x, new_y = harvester

    if move_harvester_in_direction == 'N':
        new_y -= 1
        if new_y < 0:
            return
    elif move_harvester_in_direction == 'S':
        new_y += 1
        if new_y >= world.y:
            return
    elif move_harvester_in_direction == 'E':
        new_x += 1
        if new_x >= world.x:
            return
    elif move_harvester_in_direction == 'W':
        new_x -= 1
        if new_x < 0:
            return
    if (new_x, new_y) in state.obstacle_dict:
        return state, to_observation({(x, new_y): '#'})

    new_harvester_dict = copy.copy(state.harvester_dict)
    new_food_dict = copy.copy(state.food_dict)
    new_explored_dict = copy.copy(state.explored_dict)
    new_has_food = state.has_food
    new_reward = state.reward
    new_defender_dict = copy.copy(state.defender_dict)
    remaining_food = copy.copy(state.future_food)

    del new_harvester_dict[harvester]
    new_harvester_dict[(new_x, new_y)] = 'H'
    new_explored_dict[harvester] = '-'

    if move_defender_too:
        defender, _ = state.defender_dict.iteritems().next()
        del new_defender_dict[defender]
        new_defender_dict[(new_x, new_y)] = 'D'
        #new_explored_dict[defender] = '-'

    if state.has_food and (new_x, new_y) in state.base_dict:
        new_reward += 50

    if not state.has_food and (new_x, new_y) in state.food_dict:
        del new_food_dict[(new_x, new_y)]
        state.has_food = True
        new_explored_dict = {}
        while len(new_food_dict) < world.max_food:
            new_food, remaining_food = sample_replacement_food(remaining_food)
            new_food_dict[new_food]

    next_state = to_state(state.base_dict,
                          new_harvester_dict,
                          food=new_food_dict,
                          obstacle=state.obstacle_dict,
                          defender=new_defender_dict,
                          explored=new_explored_dict,
                          enemy=state.enemy_dict,
                          has_food=new_has_food,
                          reward=new_reward,
                          future_food=remaining_food,
                          distances=state.distances)

    return next_state, {}  # observations



    '''








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


    '''



def move(state, action, harvester_world):
    # harvester_coordinate, harvester_symbol = find_harvester(state.grid)

    # if moving the harvester
    # Where is it going?
    # Can it move at all?
    # what does it leave behind?
    # What does it do to whatever is already there?

        #new_from_symbol = leaving_symbol(harvester_symbol)
        #new_to_coordinate = to_coordinate(harvester_coordinate, action, harvester_world)
        #to_symbol = state.grid.get(new_to_coordinate, None)

    # if moving a defender too
    # Same quesitons as above
    # return a whole new set of dictionaries

    #if to_symbol and to_symbol in '#':
    #    return (harvester_coordinate, harvester_symbol), (new_to_coordinate, to_symbol)
    #new_to_symbol = arriving(harvester_symbol, to_symbol)
    #return (harvester_coordinate, new_from_symbol), (new_to_coordinate, new_to_symbol)
    return 1


def to_coordinate(coordinate, action, harvester_world):
    x = coordinate[0]
    y = coordinate[1]
    if action in 'ND' and y - 1 >= 0:
        y += -1
    elif action in 'SD' and y + 1 < harvester_world.y:
        y += 1
    elif action in 'ED' and x + 1 < harvester_world.x:
        x += 1
    elif action in 'WD' and x - 1 >= 0:
        x += -1
    return x, y


# def leaving_symbol(from_symbol):
#     if from_symbol in 'DH$':
#         return None
#     if from_symbol in '*b':
#         return 'B'
#     if from_symbol in '!':
#         return 'F'
#     if from_symbol in 'd':  # I don't think this will work
#         return 'D'
#     return None


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


def add_food(grid, coordinate):  # Combine this with replace_food above
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
        #print(grid)
        #print("time: {0}".format(time))
        new_reward += 50 * pow(0.95, time)
    return new_reward


# def find_harvester(grid):
#     for coordinate, cell in grid.iteritems():
#         if cell and cell in 'bH*$!d':
#             return coordinate, cell
#     return None

    
# def arriving(from_symbol, to_symbol):
#     if from_symbol in '$!' and to_symbol == 'B':  # A harvester carrying food
#         return '*' # Gets a reward
#     if from_symbol in 'b*Hd' and to_symbol == 'F':
#         return '$'
#     if from_symbol in '$!' and to_symbol == 'F':
#         return '!'
#     if from_symbol in 'H' and to_symbol == 'B':
#         return 'b'  # Does not get a reward
#     if from_symbol in 'b*' and to_symbol and to_symbol in 'b*B':
#         return 'b'
#     if from_symbol in '!':
#         return '$'
#     if from_symbol in 'b*':
#         return 'H'
#
#     return from_symbol


def find_base(grid):
    for coordinate, unit in grid.iteritems():
        if unit and unit in 'Bb*':
            return coordinate, unit
    return None


def find_food(grid):
    food = []
    for coordinate, unit in grid.iteritems():
        if unit and unit in 'F!':
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
    new_food_dict = sample_max_food(belief_state, dimensions)
    if dimensions.known:
        future_food = belief_state.future_food
    else:
        future_food = sample_n_future_food(dimensions, 100)
    distances = all_distances(belief_state, dimensions)
    # to_base = distance_to_base(complete_grid, dimensions)
    # food_distances = add_distance_to_food(complete_grid, to_base, dimensions)
    # all_distances = add_distance_to_future(complete_grid, food_distances, future_food, dimensions)
    complete_state = to_state(belief_state.base_dict,
                              belief_state.harvester_dict,
                              food= new_food_dict,
                              obstacle=belief_state.obstacle_dict,
                              defender=belief_state.defender_dict,
                              enemy=belief_state.enemy_dict,
                              explored=belief_state.explored_dict,
                              has_food=belief_state.has_food,
                              reward=belief_state.reward,
                              distances=distances,
                              future_food=future_food)
    return complete_state

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
        if unit and unit in 'F!':
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
    if unit_a in 'H' and unit_b in 'F':
        return '$'
    if unit_a in '$!' and unit_b in 'F':
        return '!'
    if unit_a in '*' and unit_b in 'F':
        return '*'
    if unit_a in 'b' and unit_b in 'F':
        return 'b'
    if unit_a in '!$' and unit_b in 'B':
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


def all_distances(state, problem):
    distances = []
    for x in range(problem.x):
        for y in range(problem.y):
            if (x, y) not in state.obstacle_dict:
                distances.append(((x, y), dijkstra.dijkstra((x, y), state, problem)))
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




def sample_max_food(state, dimensions):

    #print(grid)
    new_food_dict = deepcopy(state.food_dict)
    while len(new_food_dict) < dimensions.max_food:
        #print(try_coordinate)
        try_coordinate = sample_cell(dimensions.x, dimensions.y)
        if try_coordinate not in state.base_dict \
                and try_coordinate not in state.obstacle_dict \
                and try_coordinate not in state.harvester_dict \
                and try_coordinate not in state.explored_dict:
            new_food_dict[try_coordinate] = 'F'
    return new_food_dict


def sample_replacement_food(state, future_food):
    remaining_food = copy.copy(future_food)
    while True:
        try_x = remaining_food.pop()
        try_y = remaining_food.pop()
        # print(try_x, try_y)
        remaining_food.insert(0, try_x)
        remaining_food.insert(0, try_y)
        try_coordinate = (try_x, try_y)
        if try_coordinate not in state.base_dict \
                and try_coordinate not in state.obstacle_dict \
                and try_coordinate not in state.harvester_dict \
                and try_coordinate not in state.explored_dict:
            return try_coordinate, remaining_food


def try_future_food(grid, coordinate):
    if coordinate not in grid:
        return coordinate
    if grid[coordinate] in 'Bb*#':
        return None
    if grid[coordinate] in 'H$!':
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

    
