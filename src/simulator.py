'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import problem
from collections import namedtuple

def simulate(belief_state, action, real_world, problem_spec): #TODO: Wh do I need a beleft state?
    '''
    Takes a state (a starting collection of units(?), an action, and a world (grid)  and returns a new world. Transition may not always be possible.
    '''
    #coordinate=get_coordinate(state) #TODO: I'm not sure an agent should tell the simulator everything it knows
    real_world_dict = problem.to_dict(real_world)
    new_world = problem.transition(real_world_dict, action, problem_spec)
    new_world_dict = new_world.state_dict
    new_observations = new_world.observation_dict #TODO: Return new observations to agent so it can update its belief state (overengineered?)
    #TODO: What about newly discovered obstacles?
    #TODO: Spawn new rewardable objects? But these should stay hidden
    #TODO: How does what is known change? 
    '''Spawn new rewards. What is the simplest way to spawn new rewards? Use the same model used for generating 
    inital real world (none yet). If I did have a model for generating the inital real world, what might it do? Maybe the similar
    to what I built for speculating about the world. For now, use the same model I built for speculating about the world--The 
    assumption is that the agent knows the real probability distribution (or his estimate is unbiased :). This model lives in
    the world module right now.
    '''
    probability_to_reset = problem.reset_distribution(new_world_dict, problem_spec) #TODO: Uses default problem spec for testing, create a problem spec function
    new_world_dict = problem.reset(new_world_dict, probability_to_reset) #TODO: Modify in place #TODO: Fix 1 - running total. Should not be -0.30000000000000004,
    new_world_grid = problem.to_grid(new_world_dict,problem_spec)
    Simulation = namedtuple('Simulation',['new_real_world_grid','new_observations_dict'])
    simulation = Simulation(new_world_grid, new_observations)
    return simulation #TODO: Return cumulative reward to use to compare results of each run


def get_coordinate(state): #TODO: Get rid of this during refactoring
    for coordinate, unit in state.iteritems():
        if unit in 'H*$!0': #TODO: Problem should manage identifying a unit from any of the internal encodings, when I finally settle on an encoding
            return coordinate
    return None

if __name__ == '__main__':
    pass
