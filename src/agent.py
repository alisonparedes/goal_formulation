'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import simulator
from ohwow import *
from copy import deepcopy
import os


def new_belief_state(belief_state, new_observations):
    '''
    When should an agent remove an attribute from his belief state? Never? World sample could speculate about visited states. When is belief state this fluid? Fluents are allowed to change over time.

    :param state:
    :param new_knowledge:
    :return:
    '''
    for coordinate, cell in new_observations.iteritems():
            belief_state[coordinate]=cell
    return belief_state

def get_current_state(state):
    for coordinate, cell in state.iteritems():
        if cell in 'H$*!0':
            return {coordinate:cell}
    return None

if __name__ == '__main__': #TODO: What arguments should it accept?
    real_world=[[None, None, 'F', None], ['H', None, None, None], [None, None, None, None], [None, 'B', None, None]]
    belief_state={(1, 0): 'H', (3, 1): 'B'}
    problem_spec=(len(real_world), len(real_world[0]))
    print(problem_spec)
    while True: #TODO: True may be a bit much. When to stop?
        action = ohwow(belief_state, problem_spec)
        old_world = deepcopy(real_world) #TODO: Why not modify in place?
        new_world = simulator.simulate(belief_state, action[0], real_world, problem_spec) #Modifies world
        new_observations = new_world.new_observations_dict
        new_world_state = new_world.new_real_world_grid
        belief_state = new_belief_state(belief_state, new_observations)
        real_world = new_world_state
        os.system('clear')
        print(problem.interleaved(belief_state, real_world, problem_spec)) #TODO: Swap these parameters to reflect order states will be printed
