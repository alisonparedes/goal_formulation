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
import sys
import random


def update_belief(state, observation, known=False, reality_state=None):

    if not observation:
        return state
    new_grid = update_cell(state.grid, observation.dict)
    new_reward = state.reward
    if problem.found_food(state.grid, observation.dict):
        new_reward = observation.reward
        new_grid = problem.del_explored_cell(new_grid)
    future_food = None
    if known:
        future_food = reality_state.future_food
    return problem.to_state(new_grid, reward=new_reward, future_food=future_food)


def update_cell(grid, cell_dict):
    new_grid = deepcopy(grid)
    for coordinate, cell in cell_dict.iteritems():  # Set of observations is much smaller than state
        new_grid[coordinate] = cell
    return new_grid


def init_reality(reality_file_name):
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
    return problem.to_state(grid_dict), x, y


def init_belief(belief_file_name, future_food=None):
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
    base, harvester, food, obstacle, defender, enemy, has_food = problem.parse(belief_str)
    return problem.to_state(base,
                            harvester,
                            food=food,
                            obstacle=obstacle,
                            defender=defender,
                            enemy=enemy,
                            has_food=has_food,
                            future_food=future_food), x, y


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("reality")
    parser.add_argument("belief")
    parser.add_argument("horizon")
    parser.add_argument("sample")
    parser.add_argument("max_food")
    parser.add_argument("time")
    parser.add_argument("seed")
    parser.add_argument("known")
    return parser.parse_args()


def print_args(args):
    print "reality: {0}".format(args.reality)
    print "belief: {0}".format(args.belief)
    print "horizon: {0}".format(args.horizon)
    print "sample: {0}".format(args.sample)
    print "max_food: {0}".format(args.max_food)
    print "time: {0}".format(args.time)
    print "seed: {0}".format(args.seed)
    print "known: {0}".format(args.known)
    print "\n"


def print_step(time_step, state_a, state_b, dimensions):
    #os.system('clear')
    print "time: {0}".format(time_step)
    print "reward: {0}".format(state_b.reward)
    print(problem.interleaved(state_a.grid, state_b.grid, dimensions))


if __name__ == '__main__':

    args = parse_args()
    random.seed(int(args.seed))
    reality_state, x, y = init_reality(args.reality)  # Dimensions of reality are derived from input file
    harvester_world = problem.to_problem(x, y, int(args.max_food), int(args.known))
    # food_dist = problem.chance_of_food(reality_state, harvester_world)
    future_food = problem.sample_n_future_food(harvester_world, 100)
    # for i in range(1000):
    #     future_food.append(problem.sample_cell(food_dist)[1])
    reality_state = problem.to_state(reality_state.grid, future_food=future_food)

    if harvester_world.known:
        belief_state, _, _ = init_belief(args.belief, future_food=future_food)
    else:
        belief_state, _, _ = init_belief(args.belief)

    time_step = 0
    print_args(args)
    print_step(time_step, reality_state, belief_state, harvester_world)

    while time_step < int(args.time):
        #print("reality: ", reality_state)
        #print("belief: ", belief_state)
        action = ohwow.ohwow(belief_state,
                             harvester_world,
                             number_of_samples=int(args.sample),
                             horizon=int(args.horizon))
        reality_state, observations = simulator.simulate(belief_state,
                                                         action[0],
                                                         reality_state,
                                                         dimensions=harvester_world)
        #print("action: {0} observations: {1}\n", action, observations)
        #print("old belief: {0}\n", belief_state.grid)
        belief_state = update_belief(belief_state, observations, harvester_world.known, reality_state)
        #print("new belief: {0}\n", belief_state.grid)
        time_step += 1
        #time.sleep(0.25)
        print_step(time_step, reality_state, belief_state, harvester_world)
    print("total reward: {0}\n".format(belief_state.reward))
    sys.exit(0)
