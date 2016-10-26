'''
Created on Sep 2, 2016

@author: lenovo
'''
import unittest
from bfs_g import *
import problem

class Test(unittest.TestCase):

    '''
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
    '''
    '''
    def testSearch1toD20(self): #Results 9/5 (assume no dups): 1 action = 0.003s, 2=0.010s, 3=0.632s, 4=98.076s (98.365s!)
        simstate = '-H--\nF--B'
        initial_state = problem.parse(simstate)
        plan=search(initial_state,19)
        self.assertEquals(plan,[1,1,1,1,1,1,1,1,1,1],plan)
    '''
    '''
    def testSearch1toD1(self):
        initial_state = 1
        goal_state = 10
        plan=search(initial_state,goal_state,1)
        self.assertEquals(plan,[1],plan)
    '''
    '''    
    def testSearch1toGoal(self):
        initial_state = 1
        goal_state = 10
        plan=search(initial_state,goal_state,11)
        self.assertEquals(plan,[1,1,1,1,1,1,1,1,1],plan)
    '''
    def testTransition(self):
        State = namedtuple('State',['state','reward']) #TODO: Problem should handle state structure.
        Simulated = namedtuple('Simulated',['state','resources'])
        Node = namedtuple('Node',['state','previous','action', 'g'])
        i = Node(State(initial_state,0), previous=None, action=None, g=0) #TODO: How to delegate creating an initial State object to problem?
        transition(s_node, action, State, Simulated)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSearch']
    unittest.main()