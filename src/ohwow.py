'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
import bfs_g
import problem


def ohwow(belief_state, number_of_samples=1, horizon=1):
    """
    """

    sampled_worlds = sample(belief_state, number_of_samples)
    actions_in_s = problem.applicable_actions(belief_state)

    max_action = None
    max_expected_value = 0
    for action in actions_in_s:
        total_reward = 0.0
        for initial_state in sampled_worlds:
            next_state = problem.transition(initial_state, action)
            total_reward += next_state.reward
            total_reward += bfs_g.search(next_state, horizon)
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


def sample(belief_state, number_of_samples):
    sampled_worlds = []
    food_dist = problem.chance_of_food(belief_state)
    distance_to_base = problem.distance_to_base(belief_state)
    for i in range(number_of_samples):
        grid = problem.sample_food(food_dist, belief_state)
        distance = problem.add_distance_to_food(distance_to_base, belief_state)
        w = problem.to_state(grid, belief_state.reward, t=0, future_food=world.future_food, distances=distance)
        sampled_worlds.append(w)
    return sampled_worlds


if __name__ == '__main__':
    pass
