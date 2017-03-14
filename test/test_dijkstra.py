'''
Created on Aug 26, 2016

@author: lenovo
'''
import unittest
from dijkstra import *
import problem


class TestDijkstra(unittest.TestCase):

    def testDijkstra(self):
        state_str = '#-\n-b'
        base, harvester, food, obstacle, defender, enemy, has_food = problem.parse(state_str)
        state = problem.to_state(base, harvester, food, obstacle, defender, enemy, has_food)
        world = problem.to_problem(x=2, y=2)
        policy = dijkstra((1, 1), state, world)
        self.assertEquals(policy,  {(0, 1): ((1, 1), 1), (1, 0): ((1, 1), 1), (1, 1): ('*', 0)}, policy)

    def testExpand(self):
        state_str = 'H-\n-B'
        base, harvester, food, obstacle, defender, enemy, has_food = problem.parse(state_str)
        state = problem.to_state(base, harvester, food, obstacle, defender, enemy, has_food)
        world = problem.to_problem(x=2, y=2)
        open_list = []
        policy = [[None] * world.y for _ in range(world.x)]
        expand(((1, 1), 0), open_list, policy, state, world)
        self.assertEquals(open_list, [((1, 0), 1), ((0, 1), 1)],  open_list)
        self.assertEquals(policy,  [[None, ((1, 1), 1)], [((1, 1), 1), None]], policy)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()