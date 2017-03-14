'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from agent import *
import problem
from collections import namedtuple


class TestAgent(unittest.TestCase):

    def testInitReality(self):
        file_name = "/home/aifs2/alison/IdeaProjects/goal_formulation/test/tiny_01.txt"
        reality, x, y = init_reality(file_name)
        self.assertEquals(reality.grid, {(0, 0): 'F', (1, 1): 'b'}, reality.grid)
        self.assertEquals(reality.reward, 0, reality.reward)
        self.assertEquals(reality.t, 0, reality.t)
        self.assertEquals(reality.future_food, [], reality.future_food)
        self.assertEquals(x, 2, x)
        self.assertEquals(y, 2, y)

    def testInitBelief(self):
        file_name = "/home/aifs2/alison/IdeaProjects/goal_formulation/test/tiny_01.txt"
        belief, _, _ = init_belief(file_name)
        self.assertDictEqual(belief.base_dict, {(1, 0): 'b'}, belief.base_dict)
        self.assertDictEqual(belief.harvester_dict, {(1, 0): 'b'}, belief.harvester_dict)
        self.assertDictEqual(belief.food_dict, {(2, 0): 'F'}, belief.food_dict)
        self.assertDictEqual(belief.obstacle_dict, {(3, 0): '#'}, belief.obstacle_dict)
        self.assertDictEqual(belief.defender_dict, {(4, 0): 'D'}, belief.defender_dict)
        self.assertDictEqual(belief.enemy_dict, {(5, 0): 'E'}, belief.enemy_dict)
        self.assertDictEqual(belief.explored_dict, {}, belief.explored_dict)
        self.assertEquals(belief.has_food, False, belief.has_food)
        self.assertEquals(belief.reward, 0, belief.reward)
        self.assertEquals(belief.future_food, None, belief.future_food)


    def testListExploredCell(self):
        belief_str = 'F-\n-b'
        grid = problem.parse(belief_str)
        grid[(1, 0)] = '-'
        grid[(0, 1)] = '-'
        explored = list_explored_cell(grid)
        self.assertEquals(explored, {(1, 0): '-',  (0, 1): '-'}, explored)

    def testDelExploredCell(self):
        belief_str = 'F-\n-b'
        grid = problem.parse(belief_str)
        grid[(1, 0)] = '-'
        grid[(0, 1)] = '-'
        new_grid = del_explored_cell(grid)
        self.assertEquals(new_grid, {(0, 0): 'F', (1, 1): 'b'}, new_grid)
        self.assertEquals(grid, {(0, 0): 'F', (1, 1): 'b', (1, 0): '-',  (0, 1): '-'}, grid)

    def testUpdateCell(self):
        belief_str = 'F-\n-b'
        grid = problem.parse(belief_str)
        observation_str = '--\nHB'
        observation_dict = problem.parse(observation_str)
        new_grid = update_cell(grid, observation_dict)
        self.assertEquals(new_grid, {(0, 0): 'F',  (1, 1): 'B', (0, 1): 'H'}, new_grid)
        self.assertEquals(grid, {(0, 0): 'F', (1, 1): 'b'}, grid)

    def testIsPayDay(self):
        belief_str = 'F-\n-*'
        grid = problem.parse(belief_str)
        pay_day = is_pay_day(grid)
        self.assertEquals(pay_day, True, pay_day)

    def testUpdateBelief(self):
        belief_str = 'F-\n-b'
        grid = problem.parse(belief_str)
        belief = problem.to_state(grid)
        observation_str = '--\nHB'
        observation_dict = problem.parse(observation_str)
        observation = problem.to_observation(observation_dict)
        new_belief = update_belief(belief, observation)
        self.assertEquals(new_belief.grid, {(0, 0): 'F',  (1, 1): 'B', (0, 1): 'H'}, new_belief.grid)
        self.assertEquals(belief.grid, {(0, 0): 'F', (1, 1): 'b'}, belief.grid)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()