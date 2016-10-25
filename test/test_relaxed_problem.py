'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from relaxed_problem import *
import problem

class Test(unittest.TestCase):


    def testTransitionHB(self):
        simstate = '-H--\n---B'
        state = problem.parse(simstate)
        action = 1 #HB
        next_state = transition(state, action)
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