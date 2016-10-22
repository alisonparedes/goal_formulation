'''
Created on Aug 26, 2016

@author: lenovo
'''
import unittest
from dijkstra import *


class Test(unittest.TestCase):


    def testActions(self):
        dijkstra = UniformCostSearchTree()
        plan = dijkstra.search(1)
        expected_plan = [1,1]
        self.assertEquals(plan, expected_plan, plan)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()