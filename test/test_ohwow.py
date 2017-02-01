'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from ohwow import *
import random


class TestOhWow(unittest.TestCase):


    def testSample(self):
        random.seed(1)
        n = 1
        state_str = '-#\n-b'
        grid = problem.parse(state_str)
        harvester_world = problem.to_problem(x=2, y=2, max_food=1)
        belief_state = problem.to_state(grid)
        possible_worlds = sample(belief_state, n, harvester_world)
        world = possible_worlds[0]
        self.assertEquals(world.grid, {(1, 1): 'b', (1, 0): '#', (0, 0): 'F'}, world.grid)
        self.assertEquals(world.reward, 0, world.reward)
        self.assertEquals(world.future_food, [], world.future_food)
        self.assertEquals(world.distances, [(((1, 1), 'b'), {(0, 1): ((1, 1), 1), (0, 0): ((0, 1), 2), (1, 1): ('*', 0)}), (((0, 0), 'F'), {(0, 1): ((0, 0), 1), (0, 0): ('*', 0), (1, 1): ((0, 1), 2)}), (((0, 1), 'F'), {(0, 1): ('*', 0), (0, 0): ((0, 1), 1), (1, 1): ((0, 1), 1)})], world.distances)
        random.seed(None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()