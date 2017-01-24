'''
Created on Aug 18, 2016

@author: lenovo
'''
import unittest
from problem import *
import random

class TestState(unittest.TestCase):


    def testParse(self):
        state_str = '-H--\n---H'
        state = parse(state_str)
        self.assertDictEqual(state, {(1,0):'H', (3,1):'H'}, state)

    def testActions(self):
        state_str = '-H--\n---B'
        grid = parse(state_str)
        state = to_state(grid, x=4, y=2)
        actions = applicable_actions(state)
        self.assertEquals(actions, ['S', 'E', 'W'], actions)

    def testFindBase(self):
        simstate = '-*--\n---F'
        state = parse(simstate)
        coordinate = find_base(state)
        self.assertEquals(coordinate, ((1,0), '*'), coordinate)

    def testTransitionBeliefStateToBase(self):
        simstate = 'HB\n-F'
        problem_spec = (2,2)
        grid = parse(simstate)
        action = 'E'
        State = namedtuple('State',['grid','reward','has_food'])
        state = State(grid, reward=0, has_food=True)
        new_state_and_observations = transition(state, action, problem_spec, State)
        new_state = new_state_and_observations.state
        self.assertEquals(new_state.reward, 50, new_state_and_observations)

    def testTransitionBeliefStateGrow(self):
        simstate = 'HF'
        problem_spec = (2,1)
        grid = parse(simstate)
        action = 'E'
        State = namedtuple('State',['grid','reward','has_food'])
        state = State(grid, reward=0, has_food=False)
        new_food=(0,0)
        new_state_and_observations = transition(state, action, problem_spec, State, new_food)
        new_state = new_state_and_observations.state
        self.assertEquals(new_state.grid, {(0, 0): 'F', (1, 0): '$'}, new_state.grid)
        
    def testTransitionRealWorldFood(self):  # TODO: The real world should be more complete; every cell should be represented
        simstate = 'H-\n-F'
        problem_spec = (2,2)
        grid = parse(simstate)
        action = 'S'
        State = namedtuple('State',['grid','reward','has_food'])
        state = State(grid, reward=0, has_food = True)
        new_state_and_observations = transition(state, action, problem_spec, State)
        new_state = new_state_and_observations.state
        self.assertEquals(new_state.has_food, True, new_state.has_food)

    def testTransitionObservations(self):
        simstate = '-H--\n---F'
        problem_spec = (4,2)
        state = parse(simstate)
        action = 'S'
        new_observations = transition(state, action, problem_spec).observation_dict
        self.assertEquals(new_observations, {(1, 0): None, (1, 1): 'H'}, new_observations)

    def testTransitionReward(self):
        simstate = 'BH--\n----'
        coordinates = parse(simstate)
        action = 'W'
        State = namedtuple('State',['state','reward','has_food'])
        initial_state = State(state=coordinates,reward=0,has_food=True)
        reward = transition(initial_state, action, (4,2), State).state_dict.reward
        self.assertEquals(reward, 50, reward)
        
    def testToGrid(self):
        simstate = '-H--\n---F'
        state = parse(simstate)
        problem_spec = (4,2)
        state_grid = to_grid(state, problem_spec)
        self.assertEquals(state_grid, [[None, None], ['H', None], [None, None], [None, 'F']], state_grid)    
        
    def testChanceToGrow(self):
        simstate = '-$\n-B'
        grid = parse(simstate)
        State = namedtuple('State',['grid','has_food'])
        state = State(grid, has_food = True)
        distribution = chance_to_grow(state, problem_spec=(2,2))
        self.assertEquals(distribution,[(0.25, (0, 0), 'F'), (0.25, (0, 1), 'F'), (0.25, (1, 0), 'F'), (0.25, (1, 1), 'F'), (0.0, None)], distribution)

    def testChanceOfFoodNoHarvest(self):
        simstate = '-H\n-B'
        grid = parse(simstate)
        State = namedtuple('State',['grid','has_food'])
        state = State(grid, has_food = False)
        distribution = chance_of_food(state, problem_spec=(2,2))
        self.assertEquals(distribution,[(0.50, (0, 0), 'F'), (0.50, (0, 1), 'F'), (0.0, None)], distribution)

    def testChanceOfFoodHasHarvest(self):
        simstate = '-$\n-B'
        grid = parse(simstate)
        State = namedtuple('State',['grid','has_food'])
        state = State(grid, has_food = True)
        distribution = chance_of_food(state, problem_spec=(2,2))
        self.assertEquals(distribution,[(0.125, (1, 0), 'F'), (0.125, (1, 1), 'F'), (0.375, (0, 0), 'F'), (0.375, (0, 1), 'F'), (0.0, None)], distribution)


    def testResetDistribution(self):
        simstate = '-H--\n---B'
        state_dict = parse(simstate)
        reset_dist = reset_distribution(state_dict)
        expected = [(0.0, (3, 1), 'B'), (0.1, (0, 0), 'F'), (0.1, (0, 1), 'F'), (0.1, (1, 1), 'F'), (0.1, (2, 0), 'F'), (0.1, (2, 1), 'F'), (0.1, (3, 0), 'F'), (0.4, None)]
        self.assertEquals(reset_dist, expected, reset_dist)
        
    def testReset(self):
        random.seed(1) #Set-up
        simstate = '-H--\n---B'
        state_dict = parse(simstate)
        state_grid = to_grid(state_dict, 4, 2)
        reset_dist = [(0.0, (3, 1), 'B'), (0.1, (0, 0), 'F'), (0.1, (0, 1), 'F'), (0.1, (1, 1), 'F'), (0.1, (2, 0), 'F'), (0.1, (2, 1), 'F'), (0.1, (3, 0), 'F'), (0.4, None)]
        new_world = reset(state_grid, reset_dist, 1)
        self.assertEquals(new_world,{(0, 1): 'F', (1, 0): 'H', (3, 1): 'B'}, new_world)
        random.seed(None) #Tear down          
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()