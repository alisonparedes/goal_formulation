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

    if not new_observations:
        return belief_state

    new_belief_state = belief_state.grid
    accumulated_reward = belief_state.reward + new_observations.reward
    reset_cells = []
    for coordinate, cell in new_observations.observation_dict.iteritems():

        # There should be be very few observations compared to the coordinates in a belief state
        new_belief_state[coordinate] = cell
        if cell == '*':
            for coordinate, cell in new_belief_state.iteritems():
                if cell == '-':
                    reset_cells.append(coordinate)

    if len(reset_cells) > 0:
        for cell in reset_cells:
            del new_belief_state[cell]

    return State(new_belief_state, accumulated_reward, t=0)


if __name__ == '__main__': #TODO: Read an initial beilef state and real world from a file

    # Scenario used for development
    '''real_world_dict=problem.to_dict([[None, None, None, None], [None, None, 'H', None], [None, None, None, None], ['B', 'F', None, 'F']])
    State = namedtuple('State',['grid','reward','has_food']) #TODO: Problem should handle state structure.
    reward=0
    has_food=False
    belief_state=State({(3, 0): 'B', (1, 2): 'H'}, reward, has_food)
    real_world=State(real_world_dict, reward, has_food)
    problem_spec=(4, 4)'''

    '''
    # Base case used for development
    # Since agent has food already it should march straight to the base with it for a reward.
    initial_state = '$---\n----\n----\n---B\n'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    #has_food=True
    belief_state=State(grid, reward)
    real_world=State(grid, reward)
    '''

    '''
    # Base case used for development
    # Agent knows about a food. It should go directly to the food then to the base with it for a reward.
    initial_state = 'H--B\n----\n----\n---F\n'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Scenario 1 used for development
    # Agent knows about a food but there is another hidden food along the way. It should go directly to the food,
    # stumble on the closer food and take that to the base with it for a reward.
    initial_state = 'H--B\nF---\n----\n---F\n'
    belief_state = 'H--B\n----\n----\n---F\n'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward, )
    '''

    '''
    # Scenario 2 used for development
    # Agent must explore for food and take it to base. Simulator grows new food, so this scenario is endlessly
    # repeatable
    initial_state = 'H--B\nF---\n----\n---F\n'
    belief_state = 'H--B\n----\n----\n----\n'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Scenario 2 with obstacles used for development
    # Agent can't move harvester past obstacle.
    initial_state = '$-#B'
    belief_state = '$--B'
    problem_spec = (4,1)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Scenario 2 with obstacles used for development
    # Agent uses policy to calculate distance to base
    initial_state = '$--\n-#B'
    belief_state = '$--\n-#B'
    problem_spec = (3,2)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Scenario 2 with obstacles used for development
    # Agent uses policy to calculate distance to any food
    initial_state = 'H#F\n---\n-#B'
    belief_state = 'H#F\n---\n-#B'
    problem_spec = (3,3)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward','has_food'])
    reward=0
    has_food=False
    belief_state=State(grid_belief, reward, has_food)
    real_world=State(grid, reward, has_food)
    '''

    '''
    # Scenario 2 with obstacles used for development
    # Agent must imagine food
    initial_state = 'H#F\nF--\n-#B'
    belief_state = 'H--\n---\n--B'
    problem_spec = (3,3)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''

    '''
    # Scenario 2 with obstacles used for development
    # Agent must explore. Bigger map.
    initial_state = 'H-F-\nF##-\n----\n--#B'
    belief_state = 'H---\n----\n----\n---B'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    # Scenario 2 for debugging
    # Agent must explore from base.
    initial_state = '--F-\nF##-\n----\n###b'
    belief_state = '----\n----\n----\n###b'
    problem_spec = (4,4)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward','t'])
    reward=0
    belief_state=State(grid_belief, reward, t=0)
    real_world=State(grid, reward, t=0)


    '''
    # Scenario 1 used for debugging
    # Agent knows about a food but there is another hidden food along the way. It should go directly to the food,
    # stumble on the closer food and take that to the base with it for a reward.
    initial_state = 'HB\nFF\n'
    belief_state = 'HB\n-F\n'
    problem_spec = (2,2)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''

    '''
    # Scenario 1 used for debugging
    # Agent must imagine food
    initial_state = 'HB\nFF\n'
    belief_state = 'HB\n--\n'
    problem_spec = (2,2)
    grid = problem.parse(initial_state)
    grid_belief = problem.parse(belief_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid_belief, reward)
    real_world=State(grid, reward)
    '''


    '''
    # Base case used to debug reward
    # Since agent has food already it should march straight to the base with it for a reward.
    initial_state = '$B\n'
    problem_spec = (2,1)
    grid = problem.parse(initial_state)
    State = namedtuple('State',['grid','reward'])
    reward=0
    belief_state=State(grid, reward)
    real_world=State(grid, reward)
    '''


    time = 0
    print "time: {0}".format(time)
    print "reward: {0}".format(real_world.reward)
    print(problem.interleaved(belief_state.grid, real_world.grid, problem_spec))
    while time <= 100:
        #print 'belief: {0}'.format(belief_state)
        action = ohwow(belief_state, problem_spec, State, n=1, horizon=4)
        new_world = simulator.simulate(belief_state, action[0], real_world, problem_spec, State)
        new_observations = new_world.observations
        real_world = new_world.state
        belief_state = new_belief_state(belief_state, new_observations)
        #os.system('clear')
        time += 1
        print "time: {0}".format(time)
        print "total reward: {0}".format(belief_state.reward)
        print(problem.interleaved(belief_state.grid, real_world.grid, problem_spec))



