'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from ohwow import *
import random


class Test(unittest.TestCase):


    def testSample(self):
        random.seed(1) #Set-up
        n = 2 #What is a good sample size?
        problem_dist = [(0.5, (0, 0), 'F'),(0.5, None)]
        belief_state={(0,1):'H',(3,3):'B'}
        possible_worlds = sample(belief_state, problem_dist, n)
        self.assertEquals(possible_worlds,[{(0, 1): 'H', (0, 0): 'F', (3, 3): 'B'}, {(0, 1): 'H', (3, 3): 'B'}],possible_worlds)
        random.seed(None) #Tear down

    def testApplicableActions(self):
        random.seed(1) #Set-up
        n = 10 #What is a good sample size?
        problem_dist = [(0.5, (0, 0), 'F'),(0.5, None)]
        belief_state={(1,1):'H',(3,3):'B'}
        actions_in_s = applicable_actions(belief_state) 
        self.assertEquals(actions_in_s,['N', 'S', 'E', 'W'],actions_in_s)       
        random.seed(None) #Tear down
        
    def testTransition(self):
        random.seed(1) #Set-up
        belief_state={(1,1):'H',(3,3):'B'}
        action='N'
        world={(1, 1): 'H', (0, 0): 'F', (3, 3): 'B'}
        s_prime = transition(belief_state, action, world)
        self.assertEquals(s_prime ,{(1, 0): 'H', (0, 0): 'F', (3, 3): 'B'},s_prime)       
        random.seed(None) #Tear down       
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()