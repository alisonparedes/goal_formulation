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
def simulate(belief_state, action, real_world, problem): #TODO: Wh do I need a beleft state?
    '''
    Takes a state (a starting collection of units(?), an action, and a world (grid)  and returns a new world. Transition may not always be possible.
    '''
    #coordinate=get_coordinate(state) #TODO: I'm not sure an agent should tell the simulator everything it knows
    distribution = problem.chance_of_food(real_world, problem_spec)
    new_foods = []
    for i in range(10):
        new_foods.append(world.sample_cell(distribution)[1])
    new_world = problem.transition(real_world, action, problem_spec, State, new_foods, maxfood)
    new_world_dict = new_world.state.grid # TODO: If state returns a dictionary then state_dict is a misnomer.
    new_observations = new_world.observations
    #TODO: What about newly discovered obstacles?
    Simulation = namedtuple('Simulation',['state','observations'])
    simulation = Simulation(State(new_world_dict, new_world.state.reward, t=0), new_observations)
    return simulation #TODO: Return cumulative reward to use to compare results of each run


if __name__ == '__main__':
    pass
