'''
Created on Aug 18, 2016

@author: lenovo
'''
import unittest
from problem import *
import random

class TestState(unittest.TestCase):


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
        harvester = find_harvester(state)
        self.assertEquals(harvester, ((1, 0), '*'), harvester)

    def testCalculateDistance(self):
        state_str = '-*--\n---F'
        state = parse(state_str)
        coordinate = find_base(state)
        self.assertEquals(coordinate, ((1, 0), '*'), coordinate)

    def testTransitionBeliefStateToBase(self):
        simstate = 'HB\n-F'
        problem_spec = (2,2)
        grid = parse(simstate)
        action = 'E'
        State = namedtuple('State', ['grid','reward','has_food'])
        state = State(grid, reward=0, has_food=True)
        new_state_and_observations = transition(state, action, problem_spec, State)
        new_state = new_state_and_observations.state
        self.assertEquals(new_state.reward, 50, new_state_and_observations)

    def testTransitionBeliefStateGrow(self):
        simstate = 'HF'
        problem_spec = (2,1)
        grid = parse(simstate)
        action = 'E'
        State = namedtuple('State',['grid','reward','has_food'])
        state = State(grid, reward=0, has_food=False)
        new_food=(0,0)
        new_state_and_observations = transition(state, action, problem_spec, State, new_food)
        new_state = new_state_and_observations.state
        self.assertEquals(new_state.grid, {(0, 0): 'F', (1, 0): '$'}, new_state.grid)
        
    def testTransitionRealWorldFood(self):  # TODO: The real world should be more complete; every cell should be represented
        simstate = 'H-\n-F'
        problem_spec = (2,2)
        grid = parse(simstate)
        action = 'S'
        State = namedtuple('State',['grid','reward','has_food'])
        state = State(grid, reward=0, has_food = True)
        new_state_and_observations = transition(state, action, problem_spec, State)
        new_state = new_state_and_observations.state
        self.assertEquals(new_state.has_food, True, new_state.has_food)

    def testTransitionObservations(self):
        simstate = '-H--\n---F'
        problem_spec = (4,2)
        state = parse(simstate)
        action = 'S'
        new_observations = transition(state, action, problem_spec).observation_dict
        self.assertEquals(new_observations, {(1, 0): None, (1, 1): 'H'}, new_observations)

    def testTransitionReward(self):
        simstate = 'BH--\n----'
        coordinates = parse(simstate)
        action = 'W'
        State = namedtuple('State',['state','reward','has_food'])
        initial_state = State(state=coordinates,reward=0,has_food=True)
        reward = transition(initial_state, action, (4,2), State).state_dict.reward
        self.assertEquals(reward, 50, reward)
        
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
        state = to_state(grid)
        harvester_world = to_problem(x=2, y=2)
        distance = distance_to_base(state, harvester_world)
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
        state = to_state(grid)
        harvester_world = to_problem(x=2, y=2)
        distance = []
        distance = add_distance_to_food(distance, state, harvester_world)
        expected_distance = [(((1, 1), 'F'), {(0, 1): ((1, 1), 1), (0, 0): ((0, 1), 2), (1, 1): ('*', 0)})]
        self.assertEquals(distance, expected_distance, distance)

    def testToProblem(self):
        pass
        # harvester_world = to_problem(1, 2, 3)
        # self.assertEquals(harvester_world.max_food, 1, harvester_world.max_food)
        # self.assertEquals(harvester_world.x, 2, harvester_world.x)
        # self.assertEquals(harvester_world.y, 3, harvester_world.y)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()