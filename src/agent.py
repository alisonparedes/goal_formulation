'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import simulator
import ohwow
import os
import argparse
import time
import problem
from copy import deepcopy


def update_belief(state, observation):
    """An agent can update its own belief state about the location of objects in the world and how much reward it has
    accumulated so far.
    :param state: A state object representing the agent's current belief state
    :param observation: An observation object
    :return Agent's new belief state
    """
    if not observation:
        return state
    new_grid = update_cell(state.grid, observation.cell_dict)
    new_reward = state.reward
    if is_pay_day(observation.cell_dict):
        new_grid = del_explored_cell(new_grid)
        new_reward += observation.reward
    return problem.to_state(new_grid, reward=new_reward)


def del_explored_cell(grid):
    explored = list_explored_cell(grid)
    new_grid = deepcopy(grid)
    for coordinate, _ in explored.iteritems():
        del new_grid[coordinate]
    return new_grid


def list_explored_cell(grid):
    explored = {}
    for coordinate, cell in grid.iteritems():
        if cell == '-':
            explored[coordinate] = cell
    return explored


def update_cell(grid, cell_dict):
    new_grid = deepcopy(grid)
    for coordinate, cell in cell_dict.iteritems():  # Set of observations is much smaller than state
        new_grid[coordinate] = cell
    return new_grid


def is_pay_day(cell_dict):
    for coordinate, cell in cell_dict.iteritems():
        if cell == '*':
            return True


def init_reality(reality_file_name, other_args):
    """Constructs the initial state of the world from a file.
    param: reality_file_name: The path and name of a file illustrating the real world. See problem for format.
    return: Initial state of the world
    return: x, y: Dimensions of the world
    """
    reality_str = ''
    x = 0
    y = 0
    with open(reality_file_name, 'r') as reality_file:
        for line in reality_file:
            reality_str += line
            x = len(line) - 1
            y += 1
    grid_dict = problem.parse(reality_str)
    return problem.to_state(grid_dict, x, y, max_food=int(other_args.max_food))


def init_belief(belief_file_name, other_args):
    """Constructs the agent's initial belief about the world from a file.
    param: belief_file_name: The path and name of a file illustrating the agent's belief. See problem for format.
    return: Agent's initial belief state
    """
    belief_str = ''
    x = 0
    y = 0
    with open(belief_file_name, 'r') as belief:
        for line in belief:
            belief_str += line
            x = len(line) - 1
            y += 1
    grid_dict = problem.parse(belief_str)
    return problem.to_state(grid_dict, x, y, max_food=int(other_args.max_food))



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("reality")
    parser.add_argument("belief")
    parser.add_argument("horizon")
    parser.add_argument("sample")
    parser.add_argument("max_food")
    parser.add_argument("time")
    return parser.parse_args()


def print_args(args):
    print "reality: {0}".format(args.real)
    print "belief: {0}".format(args.belief)
    print "horizon: {0}".format(args.horizon)
    print "sample: {0}".format(args.sample)
    print "max_food: {0}".format(args.food)
    print "time: {0}".format(args.time)


def print_step(time_step, state_a, state_b, dimensions):
    os.system('clear')
    print "time: {0}".format(time_step)
    print "reward: {0}".format(state_b.reward)
    print(problem.interleaved(state_a.grid, state_b.grid, dimensions))


if __name__ == '__main__':

    args = parse_args()
    reality_state, x, y = init_reality(args.real)  # Dimensions of reality are derived from input file
    belief_state = init_belief(args.belief)

    time_step = 0
    print_step(time_step, belief_state, reality_state)

    while time_step < int(args.time):

        action = ohwow.ohwow(belief_state, n=int(args.sample), horizon=int(args.horizon))
        new_world = simulator.simulate(belief_state, action[0], reality_state)
        new_observations = new_world.observations
        real_world = new_world.state
        belief_state = update_belief(belief_state, new_observations)

        time_step += 1
        time.sleep(0.25)
        print_step(time_step, belief_state, reality_state)

