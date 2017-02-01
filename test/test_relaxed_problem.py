'''
Created on Oct 25, 2016

@author: lenovo
'''
import unittest
from relaxed_problem import *
import problem
import random


class TestRelaxedProblem(unittest.TestCase):

    def testTransitionHB(self):
        state_str = '---$\n---B'
        grid = problem.parse(state_str)
        action = 'HB'
        harvester_world = problem.to_problem(x=4, y=2)
        distances = problem.distance_to_base(grid, harvester_world)
        initial_state = problem.to_state(grid, distances=distances)
        next_state, action_cost = transition(initial_state, action, harvester_world, time_left=1)
        self.assertEquals(next_state.grid, {(3, 1): '*', (3, 0): None}, next_state.grid)
        self.assertEquals(next_state.reward, 49, next_state.reward)
        self.assertEquals(action_cost, 1, action_cost)
        
    def testTransitionHF(self):
        state_str = 'B---\n--HF'
        grid = problem.parse(state_str)
        action = 'HF_3_1'
        harvester_world = problem.to_problem(x=4, y=2)
        distances = problem.distance_to_base(grid, harvester_world)
        distances = problem.add_distance_to_food(grid, distances, harvester_world)
        initial_state = problem.to_state(grid, distances=distances)
        next_state, action_cost = transition(initial_state, action, harvester_world, time_left=1)
        self.assertEquals(next_state.grid, {(0, 0): 'B', (3, 1): '$', (2, 1): None}, next_state.grid)
        self.assertEquals(next_state.reward, -1, next_state.reward)
        self.assertEquals(action_cost, 1, action_cost)

    def testTransitionHFMaxFood1(self):
        random.seed(1)
        state_str = 'B---\n--HF'
        grid = problem.parse(state_str)
        action = 'HF_3_1'
        harvester_world = problem.to_problem(x=4, y=2, max_food=1)
        distances = problem.distance_to_base(grid, harvester_world)
        distances = problem.add_distance_to_food(grid, distances, harvester_world)
        belief_state = problem.to_state(grid, distances=distances)
        food_dist = problem.chance_of_food(belief_state, harvester_world)
        future_food = problem.sample_future_food(food_dist, n=1)
        initial_state = problem.to_state(grid, distances=distances, future_food=future_food)
        next_state, action_cost = transition(initial_state, action, harvester_world, time_left=1)
        self.assertEquals(next_state.grid, {(0, 1): 'F', (0, 0): 'B', (3, 1): '$', (2, 1): None}, next_state.grid)
        self.assertEquals(next_state.reward, -1, next_state.reward)
        self.assertEquals(action_cost, 1, action_cost)
        random.seed(None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()