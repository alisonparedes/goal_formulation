'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import simulator
from ohwow import *
from copy import deepcopy
import os

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

    new_belief_state=belief_state.grid
    has_food = new_observations.has_food

    for coordinate, cell in new_observations.observation_dict.iteritems():  # TODO: This doesn't need to be a dictionary

        # There should be be very few observations compared to the coordinates in a belief state
        new_belief_state[coordinate] = cell

        # TODO: Consider implementing this via problem
        if cell in '$':
            has_food = True
        elif cell in '*':
            has_food = False

    # TODO: These three components could be organized using a tuple using lambdas to name indices instead of
    # namedtuples, which require passing instances of the namedtuple around.
    return State(new_belief_state, belief_state.reward, has_food)


if __name__ == '__main__': #TODO: Read an initial beilef state and real world from a file

    real_world_dict=problem.to_dict([[None, None, None, None], [None, None, 'H', None], [None, None, None, None], ['B', 'F', None, 'F']])
    State = namedtuple('State',['grid','reward','has_food']) #TODO: Problem should handle state structure.
    reward=0
    has_food=False
    belief_state=State({(3, 0): 'B', (1, 2): 'H'}, reward, has_food)
    real_world=State(real_world_dict, reward, has_food)
    problem_spec=(4, 4)

    while True:
        #print 'belief: {0}'.format(belief_state)
        action = ohwow(belief_state, problem_spec, State)
        new_world = simulator.simulate(belief_state, action[0], real_world, problem_spec, State)
        new_observations = new_world.observations
        real_world = new_world.state
        belief_state = new_belief_state(belief_state, new_observations) #Does observation contain food? Nope. Fix this.
        #os.system('clear')
        print(problem.interleaved(belief_state.grid, real_world.grid, problem_spec)) #TODO: Swap these parameters to reflect order states will be printed
