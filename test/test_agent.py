'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from agent import *
import problem

class Test(unittest.TestCase):


    def testNewBeliefState(self):
        belief_state_str = '-H--\n---B'
        belief_state_dict = problem.parse(belief_state_str)
        new_observation_str = '----\n-H--'
        new_observations_dict = problem.parse(new_observation_str)
        new_observations_dict[(1,0)]=None
        new_belief_state_dict = new_belief_state(belief_state_dict, new_observations_dict)
        self.assertEquals(new_belief_state_dict, {(1, 0): None, (3, 1): 'B', (1, 1): 'H'}, new_belief_state_dict)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()