'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import simulator
from ohwow import *
from copy import deepcopy
import os
import argparse
import time

'''
   A belief state is made up of 1) a collection of coordinates and their contents, 2) the amount of reward collected so
   far and 3) the condition of having food. Coordinates could be implemented as a list of tuples instead of a
   dictionary, and operators would wrap and unwrap coordinates using either the coordinate as the key. The amount of
   reward collected is an integer. The condition of having food or not is either True or False.

   :param state:
   :param new_knowledge:
   :return:
   '''


def new_belief_state(belief_state, new_observations):

    if not new_observations:
        return belief_state

    new_belief_state = belief_state.grid
    accumulated_reward = belief_state.reward + new_observations.reward
    reset_cells = []
    for coordinate, cell in new_observations.observation_dict.iteritems():

        # There should be be very few observations compared to the coordinates in a belief state
        new_belief_state[coordinate] = cell
        if cell == '*':
            for coordinate, cell in new_belief_state.iteritems():
                if cell == '-':
                    reset_cells.append(coordinate)

    if len(reset_cells) > 0:
        for cell in reset_cells:
            del new_belief_state[cell]

    return State(new_belief_state, accumulated_reward, t=0)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("real")
    parser.add_argument("belief")
    parser.add_argument("horizon")
    parser.add_argument("sample")
    parser.add_argument("food")
    parser.add_argument("time")
    args = parser.parse_args()

    initial_state = ''
    y = 0
    x = 0
    with open(args.real, 'r') as real:
        for line in real:
            initial_state += line
            x = len(line) - 1
            y += 1
    grid = problem.parse(initial_state)
    problem_spec = (x, y)

    belief_state = ''
    with open(args.belief, 'r') as belief:
        for line in belief:
            belief_state += line

    grid_belief = problem.parse(belief_state)

    State = namedtuple('State',['grid','reward','t'])
    reward = 0
    belief_state=State(grid_belief, reward, t=0)
    real_world=State(grid, reward, t=0)
    time_step = 0
    print "time: {0}".format(time_step)
    print "reward: {0}".format(real_world.reward)
    print(problem.interleaved(belief_state.grid, real_world.grid, problem_spec))
    while time_step < int(args.time):
        #print 'belief: {0}'.format(belief_state)
        action = ohwow(belief_state, problem_spec, State, n=int(args.sample), horizon=int(args.horizon), maxfood=int(args.food))
        new_world = simulator.simulate(belief_state, action[0], real_world, problem_spec, State, maxfood=int(args.food))
        new_observations = new_world.observations
        real_world = new_world.state
        belief_state = new_belief_state(belief_state, new_observations)
        time.sleep(0.25)
        os.system('clear')
        time_step += 1
        print "time: {0}".format(time_step)
        print "total reward: {0}".format(belief_state.reward)
        print(problem.interleaved(belief_state.grid, real_world.grid, problem_spec))

    print "real: {0}".format(args.real)
    print "belief: {0}".format(args.belief)
    print "horizon: {0}".format(args.horizon)
    print "sample: {0}".format(args.sample)
    print "food: {0}".format(args.food)
    print "time: {0}".format(args.time)

