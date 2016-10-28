'''
Created on Aug 18, 2016

@author: lenovo
'''
import unittest
from problem import *
import random

class TestState(unittest.TestCase):


    def testParse(self):
        simstate = '-H--\n---H'
        state = parse(simstate)
        self.assertDictEqual(state, {(1,0):'H', (3,1):'H'}, state)
        
    '''
    def testWrite(self):
        init = ' !\n   *'
        simstate = write(parse(init))
        self.assertEquals(simstate, '\n{0}\n'.format(init), simstate) #TODO: These look equivalent to me
    '''
    def testActions(self):
        simstate = '-H--\n---B'
        state = parse(simstate)
        actions = applicable_actions(state, 2, 4)
        self.assertEquals(actions, ['S','E','W'], actions)
        
    def testGetCoordinate(self):
        simstate = '-H--\n---F'
        state = parse(simstate)
        state_grid = to_grid(state, 4, 2)
        coordinate = get_coordinate(state)
        self.assertEquals(coordinate, (1,0), coordinate)
        
    def testTransitionBeliefState(self):
        simstate = '-H--\n---F'
        state = parse(simstate)
        action = 'S'
        new_state = transition(state, action)
        self.assertEquals(new_state, {(3, 1): 'F', (1, 1): 'H'}, new_state)
        
    def testTransitionRealWorld(self): #TODO: The real world is just more complete, every cell is represented.
        simstate = '-H--\n---F'
        state = parse(simstate)
        action = 'S'
        new_state = transition(state, action)
        self.assertEquals(new_state, {(0, 0): None}, new_state)
        
    def testToGrid(self):
        simstate = '-H--\n---F'
        state = parse(simstate)
        state_grid = to_grid(state)
        self.assertEquals(state_grid, [[None, None], ['H', None], [None, None], [None, 'F']], state_grid)    
        
    def testProblemDistribution(self):
        simstate = '-H--\n---B'
        belief_state_dict = parse(simstate)
        problem_dist = problem_distribution(belief_state_dict, problem_spec=(4,2))
        self.assertEquals(problem_dist,[], problem_dist)
        
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