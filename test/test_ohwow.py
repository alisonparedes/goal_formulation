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
        harvester_world = problem.to_problem(x=4, y=4, max_food=1)
        belief_state = problem.to_state({(0, 1):'H',(3, 3):'B'})
        possible_worlds = sample(belief_state, n, harvester_world)
        world = possible_worlds[0]
        self.assertEquals(world.grid, {(0, 1): 'H', (3, 3): 'B', (0, 2): 'F'}, world.grid)
        self.assertEquals(world.reward, 0, world.reward)
        self.assertEquals(world.future_food, [], world.future_food)
        self.assertEquals(world.t, 0, world.t)
        self.assertEquals(world.distances, [], world.distances)
        random.seed(None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()