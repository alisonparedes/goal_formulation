'''
Created on Sep 2, 2016

@author: lenovo
'''
import unittest
from bfs_g import *
import problem

class TestBFSG(unittest.TestCase):

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

    def testReturnMaxG(self):
        state_str = '-#\n$B'
        grid = problem.parse(state_str)
        harvester_world = problem.to_problem(x=2, y=2)
        initial_state = problem.to_state(grid)
        max_g = search(initial_state, harvester_world, horizon=10)
        self.assertEquals(max_g, 49.0, max_g)

    def testReturnPlan(self):
        State = namedtuple('State',['state','reward','has_food']) #TODO: Problem should handle state structure.
        Node = namedtuple('Node',['state','previous','action', 'g'])
        initial_state = State(state={(3, 0): 'B', (1, 2): 'H', (3, 2): 'F', (0, 0): 'F'}, reward=0, has_food=False)
        horizon = 10;
        plan = search(initial_state, horizon, State, True)
        self.assertEquals(plan, ['HF_3_2', 'HB', 'HF_0_0', 'HB'], plan)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSearch']
    unittest.main()