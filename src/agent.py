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
    new_belief_state=belief_state.state
    has_food = new_observations.has_food
    for coordinate, cell in new_observations.observation_dict.iteritems():
        new_belief_state[coordinate]=cell
        if cell in '$':
            has_food = True
        elif cell in '*':
            has_food = False #test
    return State(new_belief_state, belief_state.reward, has_food)

def get_current_state(state):
    for coordinate, cell in state.iteritems():
        if cell in 'H$*!0':
            return {coordinate:cell}
    return None

if __name__ == '__main__': #TODO: What arguments should it accept?
    real_world_dict=problem.to_dict([[None, None, None, None], [None, None, 'H', None], [None, None, 'F', None], ['B', None, None, 'F']])
    State = namedtuple('State',['state','reward','has_food']) #TODO: Problem should handle state structure.
    reward=0
    has_food=False
    belief_state=State({(3, 0): 'B', (1, 2): 'H'}, reward, has_food)
    real_world=State(real_world_dict, reward, has_food)
    problem_spec=(4, 4)
    while True:
        print '\nbelief: {0}'.format(belief_state)
        action = ohwow(belief_state, problem_spec, State)
        new_world = simulator.simulate(belief_state, action[0], real_world, problem_spec, State)
        new_observations = new_world.new_observations
        real_world = new_world.new_real_world_grid
        belief_state = new_belief_state(belief_state, new_observations) #Does observation contain food? Nope. Fix this.
        #os.system('clear')
        print(problem.interleaved(belief_state.state, real_world.state, problem_spec)) #TODO: Swap these parameters to reflect order states will be printed
