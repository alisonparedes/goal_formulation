'''
Created on Aug 18, 2016

@author: lenovo
'''
import unittest
from problem import *
import random

class TestProblem(unittest.TestCase):


    def testParse(self):
        state_str = '-H--\n---H'
        state = parse(state_str)
        self.assertDictEqual(state, {(1,0):'H', (3,1):'H'}, state)

    def testActions(self):
        state_str = '-H--\n---B'
        grid = parse(state_str)
        state = to_state(grid)
        harvester_world = to_problem(x=4, y=2)
        actions = applicable_actions(state, harvester_world)
        self.assertEquals(actions, ['S', 'E', 'W'], actions)

    def testFindBase(self):
        state_str = '-*--\n---F'
        state = parse(state_str)
        coordinate = find_base(state)
        self.assertEquals(coordinate, ((1, 0), '*'), coordinate)

    def testFindHarvester(self):
        state_str = '-*--\n---F'
        grid = parse(state_str)
        state = to_state(grid)
        harvester = find_harvester(state.grid)
        self.assertEquals(harvester, ((1, 0), '*'), harvester)

    def testCalculateDistance(self):
        state_str = '-*--\n---F'
        state = parse(state_str)
        coordinate = find_base(state)
        self.assertEquals(coordinate, ((1, 0), '*'), coordinate)

    def testReplaceFood(self):
        state_str = '-$\n-B'
        grid = parse(state_str)
        future_food = [(0, 0)]
        state = to_state(grid, future_food=future_food)
        harvester_world = to_problem(x=2, y=2, max_food=1)
        new_grid, remaining_food = replace_food(grid, state.future_food, harvester_world.max_food)
        self.assertEquals(new_grid,  {(1, 1): 'B', (0, 0): 'F', (1, 0): '$'})

    def testTransitionRealWorldFood(self):  # TODO: The real world should be more complete; every cell should be represented
        state_str = 'H-\nFB'
        grid = parse(state_str)
        action = 'S'
        state = to_state(grid)
        harvester_world = to_problem(x=2, y=2)
        new_state, _ = transition(state, action, harvester_world)
        self.assertEquals(new_state.grid, {(0, 1): '$', (0, 0): None, (1, 1): 'B'}, new_state.grid)

    def testTransitionObservations(self):
        simstate = '-H--\nB--F'
        grid = parse(simstate)
        state = to_state(grid)
        action = 'S'
        harvester_world = to_problem(x=4, y=2)
        _, observations = transition(state, action, harvester_world)
        self.assertEquals(observations.dict, {(1, 0): None, (1, 1): 'H'}, observations.dict)

    def testTransitionReward(self):
        state_str = 'B$--\n----'
        grid = parse(state_str)
        action = 'W'
        initial_state = to_state(grid)
        harvester_world = to_problem(x=4, y=2)
        new_state, observation = transition(initial_state, action, harvester_world)
        self.assertEquals(new_state.reward, 50, new_state.reward)
        self.assertEquals(observation.reward, 50, observation.reward)

    def testMove(self):
        state_str = 'B$--\n----'
        grid = parse(state_str)
        action = 'W'
        initial_state = to_state(grid)
        new_from_cell, new_to_cell = move(initial_state, action)
        self.assertEquals(new_from_cell, ((1,0), None), new_from_cell)
        self.assertEquals(new_to_cell, ((0,0), '*'), new_to_cell)

    def testToGrid(self):
        simstate = '-H--\n---F'
        state = parse(simstate)
        problem_spec = (4,2)
        state_grid = to_grid(state, problem_spec)
        self.assertEquals(state_grid, [[None, None], ['H', None], [None, None], [None, 'F']], state_grid)

    def testChanceOfFoodHasHarvest(self):
        state_str = '-#\n$B'
        grid = parse(state_str)
        state = to_state(grid)
        harvester_world = to_problem(x=2, y=2)
        distribution = chance_of_food(state, harvester_world)
        self.assertEquals(distribution, [(0.0, (1, 0)), (0.0, (1, 1)), (0.5, (0, 0), 'F'), (0.5, (0, 1), 'F'), (0.0, None)], distribution)

    def testUnitActions(self):
        state_str = '-H--\n---B'
        grid = parse(state_str)
        state = to_state(grid)
        harvester_world = to_problem(x=4, y=2)
        actions = unit_actions((1, 0), state, harvester_world)
        self.assertEquals(actions, ['S', 'E', 'W'], actions)

    def testNoChance(self):
        state_str = '-#--\n---B'
        grid = parse(state_str)
        state = to_state(grid)
        distribution = no_chance(state)
        self.assertEquals(distribution, [(0.0, (1, 0)), (0.0, (3, 1))], distribution)

    def testDistanceToBase(self):
        state_str = '-#\n-B'
        grid = parse(state_str)
        harvester_world = to_problem(x=2, y=2)
        distance = distance_to_base(grid, harvester_world)
        expected_distance = [(((1, 1), 'B'), {(0, 1): ((1, 1), 1), (0, 0): ((0, 1), 2), (1, 1): ('*', 0)})]
        self.assertEquals(distance, expected_distance, distance)

    def testSampleFood(self):
        state_str = '-#\n-B'
        grid = parse(state_str)
        state = to_state(grid)
        harvester_world = to_problem(x=2, y=2, max_food=2)
        food_dist = chance_of_food(state, harvester_world)
        random.seed(1)
        new_grid = sample_food(food_dist, grid, harvester_world.max_food)
        random.seed(None)
        self.assertEquals(new_grid, {(0, 1): 'F', (1, 0): '#', (0, 0): 'F', (1, 1): 'B'}, new_grid)

    def testAddDistanceToFood(self):
        state_str = '-#\n-F'
        grid = parse(state_str)

        distance = []
        distance = add_distance_to_food(grid, distance, harvester_world)
        expected_distance = [(((1, 1), 'F'), {(0, 1): ((1, 1), 1), (0, 0): ((0, 1), 2), (1, 1): ('*', 0)})]
        self.assertEquals(distance, expected_distance, distance)

    def testFoundFood(self):
        old_belief = {(1, 2): '-', (1, 3): '-', (2, 1): 'H', (1, 1): '-', (2, 2): '-', (0, 3): 'B', (0, 2): '-'}
        observation = {(3, 1): '$', (0, 3): 'B'}
        food = found_food(old_belief, observation)
        self.assertEquals(food, True, food)

    def testFoundFood(self):
        old_belief = {(1, 2): '-', (1, 3): '-', (2, 1): '$', (1, 1): '-', (2, 2): '-', (0, 3): 'B', (0, 2): '-'}
        observation = {(3, 1): '$', (0, 3): 'B'}
        food = found_food(old_belief, observation)
        self.assertEquals(food, False, food)


    def testTransitionToFood(self):
        harvester_world = to_problem(x=4, y=4, max_food=1)
        initial_state = to_state({(1, 2): '-', (1, 3): 'H', (2, 3): 'F', (1, 1): 'B'},
                                 future_food=[3, 3, 3, 2, 3, 2, 2, 1])
        new_state, _ = transition(initial_state, 'E', harvester_world)
        self.assertEquals(new_state.grid, {(1, 2): 'F', (1, 3): None, (2, 3): '$', (1, 1): 'B'}, new_state.grid)


    def testGrow(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()