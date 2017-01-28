'''
Created on Sep 3, 2015

@author: Alison
'''

from collections import deque
import problem


def dijkstra(goal_coordinate, grid, dimensions):
    open_list = deque([(goal_coordinate, 0)])   # Distance to goal is zero when starting from goal
    policy = [[None] * dimensions.y for _ in range(dimensions.x)]
    policy[goal_coordinate[0]][goal_coordinate[1]] = ('*', 0)
    while len(open_list) > 0:
        explored = open_list.popleft()  # Start from the goal coordinate
        expand(explored, open_list, policy, grid, dimensions)
    return problem.to_dict(policy)  # Always returns something, since there is no goal state, only a reward


def expand(start, open_list, policy, grid, dimensions):
    start_coordinate = start[0]
    cost = start[1]
    for direction in problem.unit_actions(start_coordinate, grid, dimensions):
        x, y = problem.adjacent_coordinate(start_coordinate, direction)
        if not policy[x][y]:
            open_list.append(((x, y), cost + 1))
            policy[x][y] = (start_coordinate, cost + 1)

        
if __name__ == '__main__':
    pass