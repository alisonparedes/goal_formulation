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
    #return [1,2]


def transition(state, action_and_coordinate, dimensions, time_left=1):  # TODO: Why does the relaxed problem need to know the horizon
    action = action_and_coordinate.split('_')[0]
    next_state = None
    if action == 'HB':
        next_state, action_cost = hb(state, time_left)
    elif action == 'HF':
        coordinate = (int(action_and_coordinate.split('_')[1]), int(action_and_coordinate.split('_')[2]))
        next_state, action_cost = hf(state, coordinate, time_left)
    future_food = deepcopy(state.future_food)
    while problem.count_food(next_state.grid) < dimensions.max_food:
        next_state, action_cost = problem.grow(next_state, future_food.pop())
    return next_state, action_cost
    #return s


def hb(state, time_left):
    """Simulates moving harvester to base.
    @returns new_state
    """
    new_grid = deepcopy(state.grid)
    harvester = problem.find_harvester(state.grid)
    new_grid[harvester[0]] = problem.leaving_symbol(harvester[1])
    base = problem.find_base(state.grid)
    step_cost = distance(harvester, base, state.distances) # Look up cost to move to base
    to_cell = base
    if (time_left - step_cost) < 0:  # If new time is past horizon then harvester stops short of base.
        distance_to_base = problem.find_distances_to_base(state.distances)[1]
        to_cell = step(harvester[0], state.grid, time_left, distance_to_base)
    arriving_unit = problem.arriving(harvester[1], to_cell[1])
    new_grid[to_cell[0]] = arriving_unit  # May not make it all the way if takes too long
    new_reward = state.reward + problem.reward(new_grid) - step_cost
    return problem.to_state(new_grid, new_reward, state.future_food), step_cost


def step(next_step, grid, time_left, distance):
    step_cost = 0
    while time_left - step_cost > 0:  # While total_cost < horizon get next step. Stops once total_cost = horizon.
        policy = distance[next_step]  # Look up policy
        next_step = policy[0]
        step_cost += 1
    if next_step in grid:
        return next_step, grid[next_step]
    else:
        return next_step, None


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




'''
Simulate moving harvester to food
'''
def hf(state, food_coordinate, distances, State, horizon):

    new_grid = deepcopy(state.grid)

    harvester = problem.find_harvester(state.grid)
    food = (food_coordinate, 'F')

    new_grid[harvester[0]] = problem.leaving(harvester[1])

    step_cost = distance(harvester, food, distances) # Look up cost to move to base
    total_cost = state.t + step_cost # If new time is past horizon then harvester stops short of base. Use distances to figure out how far it gets.
    to_cell = food
    if total_cost > horizon:
        distance_to_food = find_distances_to_food(distances, food[0])[1]
        next_step = harvester[0]
        step_cost = 0
        while(state.t + step_cost < horizon): # While total_cost < horizon get next step. Stops once total_cost = horizon.
            policy = distance_to_food[next_step] # Look up policy
            next_step = policy[0]
            step_cost += 1

        if next_step in state.grid:
            to_cell = next_step, state.grid[next_step]
        else:
            to_cell = next_step, None

    new_grid[to_cell[0]] = problem.arriving(harvester[1], to_cell[1]) # May not make it all the way if takes too long

    next_state = problem.to_state(new_grid, state.reward, state.t, state.future_food)
    new_reward = state.reward + problem.reward(next_state) - step_cost
    return problem.to_state(new_grid, new_reward, state.future_food), step_cost


if __name__ == '__main__':
    foods = [(1,1),(2,2)]
    a = deepcopy(foods)
    b = deepcopy(foods)
    a.pop()
    print "a: {0}".format(a)
    print "b: {0}".format(b)