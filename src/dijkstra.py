'''
Created on Sep 3, 2015

@author: Alison
'''

from collections import deque, namedtuple
import problem
from copy import deepcopy

'''
Expects a coordinate identifying the goal. For this project the goal could be the base or a food node.
'''


def dijkstra(goal, belief_state, problem_spec):
    open_list = deque([(goal,0)])
    policy = empty_policy(problem_spec)
    policy[goal[0]][goal[1]] = ('*', 0)
    while len(open_list) > 0:
        explored = open_list.popleft() # Start from the goal coordinate
        expand(explored, belief_state, open_list, policy, problem_spec)
    return problem.to_dict(policy) #Always returns something, since there is no goal state, only a reward


def expand(start, belief_state, open_list, policy, problem_spec):
    start_coordinate = start[0]
    cost = start[1]
    for action in problem.unit_actions(start_coordinate, belief_state, problem_spec):
        next_state=transition(start_coordinate,action)
        x=next_state[0]
        y=next_state[1]
        if policy[x][y] == None:
            open_list.append((next_state, cost + 1)) #States are coordinates
            policy[x][y] = (start_coordinate, cost + 1)


'''
'''
def empty_policy(problem):
    w=problem[0]
    h=problem[1]
    grid = []
    for i in range(w):
        grid.append([None]*h) #Meh
    return grid


def transition(state, action):
    x = y = 0
    if action == 'N':
        y = -1
    elif action == 'S':
        y = 1
    elif action == 'E':
        x = 1
    elif action == 'W':
        x = -1
    next_x=state[0] + x
    next_y=state[1] + y
    return next_x, next_y

        
if __name__ == '__main__':
    problem_spec = (2,2)
    initial_state = 'H#\n-B'
    goal=(1,1)
    grid = problem.parse(initial_state)
    State = namedtuple('State',['grid','reward','has_food'])
    reward=0
    has_food=False
    belief_state=State(grid, reward, has_food)

    print(dijkstra(goal, belief_state, problem_spec))
    