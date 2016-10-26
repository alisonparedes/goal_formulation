'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import problem

def simulate(belief_state, action, real_world): #TODO: Wh do I need a beleft state?
    '''
    Takes a state (a starting collection of units(?), an action, and a world (grid)  and returns a new world. Transition may not always be possible.
    '''
    #coordinate=get_coordinate(state) #TODO: I'm not sure an agent should tell the simulator everything it knows
    new_world = problem.transition(state, action, real_world) #TODO: OMG reorganize top level and next level operations! For now transition requires a coordinate. How much more flexible does transition need to be?
    #TODO: What about newly discovered obstacles?
    #TODO: Spawn new rewardable objects? But these should stay hidden
    #TODO: How does what is known change? 
    '''Spawn new rewards. What is the simplest way to spawn new rewards? Use the same model used for generating 
    inital real world (none yet). If I did have a model for generating the inital real world, what might it do? Maybe the similar
    to what I built for speculating about the world. For now, use the same model I built for speculating about the world--The 
    assumption is that the agent knows the real probability distribution (or his estimate is unbiased :). This model lives in
    the world module right now.
    '''
    new_world = problem.spawn(new_world) #TODO: Modify in place?
    new_world_grid = problem.to_grid(new_world,4,4) #TODO: Where could I get these dimensions from instead?
    return new_world_grid #TODO: Return cumulative reward to use to compare results of each run

def get_coordinate(state): #TODO: Get rid of this during refactoring
    for coordinate, unit in state.iteritems():
        if unit in 'H*$!0': #TODO: Problem should manage identifying a unit from any of the internal encodings, when I finally settle on an encoding
            return coordinate
    return None

if __name__ == '__main__':
    state={(1, 0): 'H', (3, 1): 'B'}
    action='W'
    real_world=[[None, None, 'F', None], ['H', None, None, None], [None, None, None, None], [None, 'B', None, None]]
    print simulate(state, action, real_world)
