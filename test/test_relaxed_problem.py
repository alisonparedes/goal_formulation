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
        state_str = '---H\n---B'
        state_dict = problem.parse(state_str)
        action = 'HB'
        State = namedtuple('State',['state','reward','has_food'])
        initial_state = State(state_dict, reward=0, has_food=False)
        next_state = transition(initial_state, action, State)
        self.assertEquals(next_state, {(3,1):'*'}, next_state)
        
    def testTransitionHF(self):
        simstate = '-H--\n---F'
        state = problem.parse(simstate)
        action = 2 #HB
        next_state = transition(state, action)
        self.assertEquals(next_state, {(3,1):'$'}, next_state)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()