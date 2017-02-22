'''
Created on Oct 25, 2016

@author: lenovo
'''
import problem
from copy import deepcopy


def applicable_actions(s): #TODO: Units (or combinations of units, e.g. fleet) takes actions so state model needs to provide quick access to units' positions.  Although if world is small enough iterating through dictionary of positions may not be that big of a problem, .e.g one harvester and one base.
    actions = []
    units = ''
    food_coordinates = []
    for coordinate, unit in s.grid.iteritems():
        if unit and unit in 'F':
            food_coordinates.append(coordinate)
        if unit and unit in 'HbBF$*':
            units += unit
    if ('H' in units or '$' in units) and ('B' in units):
        actions.append('HB')
    if ('H' in units or '*' in units or 'b' in units) and ('F' in units):
        for food_coordinate in food_coordinates:
            actions.append('HF' + '_' + str(food_coordinate[0]) + '_' + str(food_coordinate[1]))

    return actions


def transition(state, action_and_coordinate, dimensions, time_left=1):
    """

    :param state: The easiest way to construct an initial state.

    state_str = '---$\n---B'
    grid = problem.parse(state_str)
    distances = problem.distance_to_base(grid, harvester_world)
    distances = problem.add_distance_to_food(grid, distances, harvester_world)
    initial_state = problem.to_state(grid, distances=distances)

    :param action_and_coordinate: Possible actions are HB and HF_X_Y

    action = 'HB'
    action = 'HF_3_1'

    :param dimensions:

    harvester_world = problem.to_problem(x=4, y=2)

    :param time_left:

    time_left=1

    :return: next_state, action_cost

    To visually compare initial state and action
    print(problem.interleaved(state_a.grid, state_b.grid, dimensions))
    """
    new_grid = deepcopy(state.grid)
    action = action_and_coordinate.split('_')[0]
    if action == 'HB':
        from_coordinate, from_symbol, to_coordinate, to_symbol, action_cost = hb(state, time_left)
    elif action == 'HF':
        coordinate = (int(action_and_coordinate.split('_')[1]), int(action_and_coordinate.split('_')[2]))
        from_coordinate, from_symbol, to_coordinate, to_symbol, action_cost = hf(state, coordinate, time_left)
    new_grid[from_coordinate] = from_symbol
    new_grid[to_coordinate] = to_symbol
    remaining_food = deepcopy(state.future_food)
    while problem.count_food(new_grid) < dimensions.max_food:
        new_grid, _ = problem.add_food(new_grid, remaining_food.pop())

    new_reward = state.reward + problem.reward(new_grid) - action_cost
    next_state = problem.to_state(new_grid, reward=new_reward, future_food=remaining_food, distances=state.distances)
    return next_state, action_cost


def hb(state, time_left):
    """Simulates moving harvester to base.
    @returns new_state
    """
    from_coordinate, current_from_symbol = problem.find_harvester(state.grid)
    to_coordinate, to_symbol = problem.find_base(state.grid)
    step_cost = distance((from_coordinate, current_from_symbol), (to_coordinate, to_symbol), state.distances)
    if (time_left - step_cost) < 0:  # If new time is past horizon then harvester stops short of base.
        distance_to_base = problem.find_distances_to_base(state.distances)[1]
        to_coordinate, to_symbol, step_cost = step(from_coordinate, state.grid, time_left, distance_to_base)
    to_symbol = problem.arriving(current_from_symbol, to_symbol)
    from_symbol = problem.leaving_symbol(current_from_symbol)
    return from_coordinate, from_symbol, to_coordinate, to_symbol, step_cost


def step(next_step, grid, time_left, distance):
    step_cost = 0
    while time_left - step_cost > 0:
        policy = distance[next_step]
        next_step = policy[0]
        step_cost += 1
    if next_step in grid:
        return next_step, grid[next_step], step_cost
    else:
        return next_step, None, step_cost


def distance(from_cell, to_cell, distances):
    d = 1000  # Impossible

    if to_cell[1] in 'Bb*':
        distances_to_base = problem.find_distances_to_base(distances)[1]
        if from_cell[0] in distances_to_base:
            policy = distances_to_base[from_cell[0]]
            d = policy[1]
    else:
        distances_to_food = problem.find_distances_to_food(distances, to_cell[0])
        try:
            if from_cell[0] in distances_to_food[1]:
                policy = distances_to_food[1][from_cell[0]]
                d = policy[1]
        except:
            print to_cell
            print distances
    return d


def hf(state, food_coordinate, time_left):

    from_coordinate, from_symbol = problem.find_harvester(state.grid)
    to_coordinate, to_symbol = food_coordinate, 'F'
    step_cost = distance((from_coordinate, from_symbol), (to_coordinate, to_symbol), state.distances)
    if (time_left - step_cost) < 0:  # If new time is past horizon then harvester stops short of base.
        distance_to_food = problem.find_distances_to_food(state.distances, to_coordinate)[1]
        to_coordinate, to_symbol, step_cost = step(from_coordinate, state.grid, time_left, distance_to_food)
    to_symbol = problem.arriving(from_symbol, to_symbol)
    from_symbol = problem.leaving_symbol(from_symbol)
    return from_coordinate, from_symbol, to_coordinate, to_symbol, step_cost


if __name__ == '__main__':
    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("action")
    parser.add_argument("time_left")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = problem.to_problem(x, y, int(args.max_food))
    food_dist = problem.chance_of_food(initial_state, harvester_world)
    initial_state = problem.sample(initial_state, food_dist, harvester_world)
    next_state, action_cost = transition(initial_state, args.action, harvester_world, int(args.time_left))
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "action: {0}".format(args.action)
    print "action cost: {0}".format(action_cost)
    print "reward: {0}".format(next_state.reward)
    print(problem.interleaved(initial_state.grid, next_state.grid, harvester_world))
    random.seed(0)