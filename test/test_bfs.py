'''
Created on Sep 2, 2016

@author: lenovo
'''
import unittest
from bfs import *

class Test(unittest.TestCase):


    def testSearch1to2(self):
        initial_state = 1
        goal_state = 2
        plan=search(initial_state,goal_state)
        self.assertEquals(plan,[1],plan)
        
    def testSearch1to10(self):
        initial_state = 1
        goal_state = 10
        plan=search(initial_state,goal_state)
        self.assertEquals(plan,[1,1,1,1,1,1,1,1,1],plan)
        
    def testSearch1toD9(self):
        initial_state = 1
        goal_state = 10
        plan=search(initial_state,goal_state,9)
        self.assertEquals(plan,[1,1,1,1,1,1,1,1,1],plan)

    def testSearch1toD1(self):
        initial_state = 1
        goal_state = 10
        plan=search(initial_state,goal_state,1)
        self.assertEquals(plan,[1],plan)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSearch']
    unittest.main()