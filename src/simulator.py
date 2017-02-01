'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import problem
from collections import namedtuple



def simulate(belief_state, action, real_world, dimensions):
    """
    Simulate expects the state of the world and the action the agent wishes to take in this world--its action may or may not
    be fulfilled as the agent expected. The simulate function will return a new state of the
    world and a set of observations for the agent to incorporate into its belief state. The problem module's transition
    function will handle how the world changes.
    """
    distribution = problem.chance_of_food(real_world, dimensions)
    new_foods = []
    for i in range(10):
        new_foods.append(problem.sample_cell(distribution)[1])
    new_state, observations = problem.transition(real_world, action, dimensions)
    return new_state, observations


if __name__ == '__main__':
    pass
