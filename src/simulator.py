'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import problem
from collections import namedtuple


'''
Simulate expects the state of the world and the action the agent wishes to take in this world--its action may or may not
be fulfilled as the agent expected. The simulate function will return a new state of the
world and a set of observations for the agent to incorporate into its belief state. The problem module's transition
function will handle how the world changes.
'''
def simulate(belief_state, action, real_world, problem_spec, State): #TODO: Wh do I need a beleft state?
    '''
    Takes a state (a starting collection of units(?), an action, and a world (grid)  and returns a new world. Transition may not always be possible.
    '''
    #coordinate=get_coordinate(state) #TODO: I'm not sure an agent should tell the simulator everything it knows
    new_world = problem.transition(real_world, action, problem_spec, State)
    new_world_dict = new_world.state.grid # TODO: If state returns a dictionary then state_dict is a misnomer.
    new_observations = new_world.observations
    #TODO: What about newly discovered obstacles?
    '''Spawn new rewards. What is the simplest way to spawn new rewards? Use the same model used for generating 
    inital real world (none yet). If I did have a model for generating the inital real world, what might it do? Maybe the similar
    to what I built for speculating about the world. For now, use the same model I built for speculating about the world--The 
    assumption is that the agent knows the real probability distribution (or his estimate is unbiased :). This model lives in
    the world module right now.
    '''
    probability_to_reset = problem.chance_to_grow(new_world.state, problem_spec) #TODO: Uses default problem spec for testing, create a problem spec function
    new_world_dict = problem.reset(new_world_dict, probability_to_reset)  # TODO: Fix 1 - running total. Should not be -0.30000000000000004,
    Simulation = namedtuple('Simulation',['state','observations'])
    simulation = Simulation(State(new_world_dict,real_world.reward,new_world.state.has_food), new_observations)
    return simulation #TODO: Return cumulative reward to use to compare results of each run


def get_coordinate(state): #TODO: Get rid of this during refactoring
    for coordinate, unit in state.iteritems():
        if unit in 'H*$!0': #TODO: Problem should manage identifying a unit from any of the internal encodings, when I finally settle on an encoding
            return coordinate
    return None

if __name__ == '__main__':
    pass
