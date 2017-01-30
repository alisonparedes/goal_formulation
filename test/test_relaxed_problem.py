'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from relaxed_problem import *
import problem
from collections import namedtuple


class TestRelaxedProblem(unittest.TestCase):

    def testTransitionHB(self):
        state_str = '---$\n---B'
        grid = problem.parse(state_str)
        action = 'HB'
        harvester_world = problem.to_problem(x=4, y=2)
        distances = problem.distance_to_base(grid, harvester_world)
        initial_state = problem.to_state(grid, distances=distances)
        next_state, action_cost = transition(initial_state, action, harvester_world, time_left=1)
        self.assertEquals(next_state.grid, {(3, 1): '*', (3, 0): None}, next_state.grid)
        self.assertEquals(next_state.reward, 49, next_state.reward)
        self.assertEquals(action_cost, 1, action_cost)
        
    def testTransitionHF(self):
        simstate = '-H--\n---F'
        state = problem.parse(simstate)
        action = 2 #HB
        next_state = transition(state, action)
        self.assertEquals(next_state, {(3,1):'$'}, next_state)
        self.assertEquals(new_state.reward, 50, new_state.reward)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()