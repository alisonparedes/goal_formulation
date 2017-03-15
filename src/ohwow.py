'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
import bfs_g
import problem


def ohwow(belief_state, dimensions, number_of_samples=1, horizon=1):
    """
    """
    # print("Oh wow:")
    # print(belief_state.future_food)
    sampled_worlds = sample(belief_state, number_of_samples, dimensions)
    # print(summarize_sample(sampled_worlds, dimensions))
    actions_in_s = problem.applicable_actions(belief_state, dimensions)
    max_action = None
    max_expected_value = -1000
    for action in actions_in_s:

        total_reward = 0.0
        for initial_state in sampled_worlds:
            #print(action, belief_state)
            next_state, _ = problem.transition(initial_state, action, dimensions)
            print(action, next_state)
            #print(action, next_state.grid)
            #print(problem.print_grid(next_state.grid, dimensions))
            #print(problem.interleaved(initial_state.grid, next_state.grid, dimensions))
            total_reward += next_state.reward
            total_reward += bfs_g.search(next_state, dimensions, horizon)
        expected_value = total_reward/float(number_of_samples)
        #print(action, expected_value)
        if expected_value > max_expected_value:
            max_expected_value = expected_value
            max_action = action
    return max_action, max_expected_value


def sample(belief_state, number_of_samples, dimensions):
    sampled_worlds = []
    #food_dist = problem.chance_of_food(belief_state, dimensions)
    #print(food_dist)
    for i in range(number_of_samples):
        world = problem.sample(belief_state, dimensions)
        sampled_worlds.append(world)
    return sampled_worlds


def summarize_sample(possible_worlds, problem_spec):
    """A utility function that I used for debugging"""
    summary_grid=[]
    for i in range(problem_spec.x):
        summary_grid.append([])
        for j in range(problem_spec.y):
            summary_grid[i].append(0)
    for world in possible_worlds:

        for coordinate, unit in world.grid.iteritems():
            if unit and unit in 'F':
                summary_grid[coordinate[0]][coordinate[1]] += 1
    return summary_grid


if __name__ == '__main__':
    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("number_of_samples")
    args = parser.parse_args()
    belief_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = problem.to_problem(x, y, int(args.max_food))
    food_dist = problem.chance_of_food(belief_state, harvester_world)
    possible_worlds = sample(belief_state, int(args.number_of_samples), harvester_world)
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "number_of_samples: {0}".format(args.number_of_samples)
    print(summarize_sample(possible_worlds, harvester_world))
    for world in possible_worlds:
        print(problem.interleaved(world.grid, belief_state.grid, harvester_world))
    random.seed(0)
