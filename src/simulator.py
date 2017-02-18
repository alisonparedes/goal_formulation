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
    new_state, observations = problem.transition(real_world, action, dimensions)
    return new_state, observations


if __name__ == '__main__':
    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("action")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = problem.to_problem(x, y, int(args.max_food))
    food_dist = problem.chance_of_food(initial_state, harvester_world)
    initial_state = problem.sample(initial_state, food_dist, harvester_world)
    next_state, observations = simulate(initial_state, args.action, initial_state, harvester_world)
    belief_state = agent.update_belief(initial_state, observations)
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "action: {0}".format(args.action)
    print "reward: {0}".format(next_state.reward)
    print(problem.interleaved(initial_state.grid, next_state.grid, harvester_world))
    random.seed(0)
