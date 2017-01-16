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


    '''
    # Scenario 2 with obstacles used for development
    # Agent can't move harvester past obstacle.
    initial_state = '$-#B'
    belief_state = '$--B'
    problem_spec = (4,1)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Scenario 2 with obstacles used for development
    # Agent uses policy to calculate distance to base
    initial_state = '$--\n-#B'
    belief_state = '$--\n-#B'
    problem_spec = (3,2)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Scenario 2 with obstacles used for development
    # Agent uses policy to calculate distance to any food
    initial_state = 'H#F\n---\n-#B'
    belief_state = 'H#F\n---\n-#B'
    problem_spec = (3,3)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward','has_food'])
    reward=0
    has_food=False
    belief_state=State(grid_belief, reward, has_food)
    real_world=State(grid, reward, has_food)
    '''

    '''
    # Scenario 2 with obstacles used for development
    # Agent must imagine food
    initial_state = 'H#F\nF--\n-#B'
    belief_state = 'H--\n---\n--B'
    problem_spec = (3,3)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''

    '''
    # Scenario 2 with obstacles used for development
    # Agent must explore. Bigger map.
    initial_state = 'H-F-\nF##-\n----\n--#B'
    belief_state = 'H---\n----\n----\n---B'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''

    '''
    # Scenario 2 for debugging
    # Agent must explore from base.
    initial_state = '--F-\nF##-\n----\n###b'
    belief_state = '----\n----\n----\n###b'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward','t'])
    reward=0
    belief_state=State(grid_belief, reward, t=0)
    real_world=State(grid, reward, t=0)
    '''

    # Scenario 1 read file
    # Agent must explore from base.
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


    '''
    # Scenario 1 used for debugging
    # Agent knows about a food but there is another hidden food along the way. It should go directly to the food,
    # stumble on the closer food and take that to the base with it for a reward.
    initial_state = 'HB\nFF\n'
    belief_state = 'HB\n-F\n'
    problem_spec = (2,2)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''

    '''
    # Scenario 1 used for debugging
    # Agent must imagine food
    initial_state = 'HB\nFF\n'
    belief_state = 'HB\n--\n'
    problem_spec = (2,2)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Base case used to debug reward
    # Since agent has food already it should march straight to the base with it for a reward.
    initial_state = '$B\n'
    problem_spec = (2,1)
    grid = problem.parse(initial_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid, reward)
    real_world=State(grid, reward)
    '''

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

