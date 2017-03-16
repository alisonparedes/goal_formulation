'''
Created on Sep 3, 2015

@author: Alison
'''

from collections import deque
import problem


def dijkstra(goal_coordinate, state, dimensions, enemy=False):
    open_list = deque([(goal_coordinate, 0)])   # Distance to goal is zero when starting from goal
    policy = [[None] * dimensions.y for _ in range(dimensions.x)]
    policy[goal_coordinate[0]][goal_coordinate[1]] = ('*', 0)
    while len(open_list) > 0:
        explored = open_list.popleft()  # Start from the goal coordinate
        expand(explored, open_list, policy, state, dimensions, enemy)
    return problem.to_dict(policy)  # Always returns something, since there is no goal state, only a reward


def expand(start, open_list, policy, state, dimensions, enemy=False):
    start_coordinate = start[0]
    cost = start[1]
    for direction in problem.basic_actions(start_coordinate, state, dimensions, enemy):
        x, y = problem.adjacent_coordinate(start_coordinate, direction)
        if not policy[x][y]:
            open_list.append(((x, y), cost + 1))
            policy[x][y] = (start_coordinate, cost + 1)


def interleaved(policy, belief, problem_spec):
    """Output"""
    height = problem_spec[1]
    width = problem_spec[0]
    policy_grid = problem.to_grid(policy, problem_spec)
    belief_grid = problem.to_grid(belief, problem_spec)
    printable = ''
    for y in range(height):
        for x in range(width):
            cell = policy_grid[x][y]
            if cell:
                printable += str(cell[1])  # Distance to goal
            else:
                printable += 'X'
        printable += ' '
        for x in range(width):
            cell = belief_grid[x][y]
            if cell:
                printable += cell
            else:
                printable += '?'
        printable += '\n'
    return printable


if __name__ == '__main__':
    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("goal")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = problem.to_problem(x, y)
    #food_dist = problem.chance_of_food(initial_state, harvester_world)
    #initial_state = problem.sample(initial_state, food_dist, harvester_world)
    if args.goal in 'B':
        goal_coordinate, _ = problem.find_base(initial_state.grid)
    else:
        goal_coordinate = (int(args.goal.split('_')[1]), int(args.goal.split('_')[2]))
    policy = dijkstra(goal_coordinate, initial_state.grid, harvester_world)
    print "initial_state: {0}".format(args.initial_state)
    print "goal: {0}".format(args.goal)
    print(interleaved(policy, initial_state.grid, harvester_world))
    random.seed(0)