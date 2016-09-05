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
        
    def testWrite(self):
        init = ' !\n   *'
        simstate = write(parse(init))
        self.assertEquals(simstate, '\n{0}\n'.format(init), simstate) #TODO: These look equivalent to me
        
    def testActions(self):
        simstate = '-H--\n---H'
        state = parse(simstate)
        actions = applicable_actions(state)
        self.assertEquals(actions, [1], actions)
    
    def testTransition(self):
        simstate = '-H--\n---H'
        state = parse(simstate)
        action = 'M'
        next_state = write(transition(state, action))
        self.assertEquals(next_state, 2, next_state)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()