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
        self.assertEquals(simstate, '\n{0}\nReward:90\n'.format(init), simstate) #TODO: These look equivalent to me

    def testXRef(self):
        init = '\n   *\n'
        units = xref(parse(init))
        self.assertEqual(units, {'*':(3,1)}, units)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()