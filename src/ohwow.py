'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
import bfs_g
import problem


def ohwow(belief_state, dimensions, number_of_samples=1, horizon=1):
    """
    """

    sampled_worlds = sample(belief_state, number_of_samples, dimensions)
    actions_in_s = problem.applicable_actions(belief_state, dimensions)

    max_action = None
    max_expected_value = -1000
    for action in actions_in_s:
        total_reward = 0.0
        for initial_state in sampled_worlds:
            next_state, _ = problem.transition(initial_state, action, dimensions)
            total_reward += next_state.reward
            total_reward += bfs_g.search(next_state, dimensions, horizon)
        expected_value = total_reward/float(number_of_samples)
        if expected_value > max_expected_value:
            max_expected_value = expected_value
            max_action = action
    return max_action, max_expected_value


def summarize_sample(possible_worlds, problem_spec):
    summary_grid=[]
    for i in range(problem_spec[0]):
        summary_grid.append([])
        for j in range(problem_spec[1]):
            summary_grid[i].append(0)
    for world in possible_worlds:
        for coordinate, unit in world.grid.iteritems():
            if unit in 'F':
                summary_grid[coordinate[0]][coordinate[1]] += 1
    return summary_grid


def sample(belief_state, number_of_samples, dimensions):
    sampled_worlds = []
    food_dist = problem.chance_of_food(belief_state, dimensions)
    for i in range(number_of_samples):
        world = problem.sample(belief_state, food_dist, dimensions)
        sampled_worlds.append(world)
    return sampled_worlds


if __name__ == '__main__':
    pass
