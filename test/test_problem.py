'''
Created on Aug 18, 2016

@author: lenovo
'''
import unittest
from problem import *

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
        
    def to_grid(self):
        simstate = '-H--\n---F'
        state = parse(simstate)
        state_grid = to_grid(state)
        self.assertEquals(state_grid, [[None, None], ['H', None], [None, None], [None, 'F']], state_grid)    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()