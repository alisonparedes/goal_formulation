'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

from problem import *

def simulate(state, action, real_world):
    '''
    Takes a state (a starting collection of units(?), an action, and a world (grid)  and returns a new world. Transition may not always be possible.
    '''
    #Given a world, which happens to be the real world
    #Not sure about state
    #But given an action return a new state describing everything the agent should know now. TODO: Maintain a knowledge base in the agent eventually.
    coordinate=get_coordinate(state)
    new_state = transition1(coordinate, action, real_world) #TODO: OMG reorganize top level and next level operations! For now transition requires a coordinate. How much more flexible does transition need to be?
    return new_state

def get_coordinate(state):
    for coordinate, unit in state.iteritems():
        if unit in 'H*$': #TODO: Problem should manage identifying a unit from any of the internal encodings, when I finally settle on an encoding
            return coordinate
    return None

if __name__ == '__main__':
    state={(1, 0): 'H', (3, 1): 'B'}
    action='S'
    real_world=[[None, None, 'F', None], ['H', None, None, None], [None, None, None, None], [None, 'B', None, None]]
    print simulate(state, action, real_world)