'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple, deque
import relaxed_problem


def to_node(state, previous, action, g=0, time=0):
    Node = namedtuple('Node', ['state', 'previous', 'action', 'g', 'time'])
    return Node(state, previous, action, g, time)


def search(initial_state, dimensions, horizon=1, return_plan=False):
    """
    A breadth first search which keeps track of the maximum value of all nodes see up until a node exceeds the given
    time horizon.
    :param initial_state:
    :param dimensions:
    :param horizon:
    :param return_plan:
    :return:
    """
    i = to_node(initial_state, previous=None, action=None, g=0, time=0)
    open_list = deque([i])
    closed_list = deque([])
    nodes_expanded = 0
    max_g = 0
    plan = None
    while len(open_list) > 0:
        s = open_list.popleft()
        if s.time > horizon:
            break
        max_g, plan = expand(s, open_list, closed_list, max_g, dimensions, horizon)
        nodes_expanded += 1
    if return_plan:
        return get_plan(plan), max_g
    return max_g


'''
def add_open(open_list, closed_list, expanded): #Lists must be mutable
    appended = 0
    for node in expanded:
        #if node.state not in closed_list: #TODO: What if a state were represented by a dictionary of positions and objects? Encapsulate this to delegate comparison to problem module.
        open_list.append(node)
        closed_list.append(node.state)
        appended += 1
    return appended
'''


'''def is_goal(s, goal):
    if equals(s, goal): 
        return True
    return False'''


def get_plan(s):
    HEAD = 0
    i = s
    plan = []
    while i.previous:
        plan.insert(HEAD, i.action)
        i = i.previous
    return plan


def expand(s_node, open_list, closed_list, max_g, dimensions, horizon):
    expanded = []
    plan = s_node
    for action in relaxed_problem.applicable_actions(s_node.state):
        next_state, step_time = relaxed_problem.transition(s_node.state, action, dimensions, horizon)
        g = next_state.reward
        result = to_node(state=next_state, previous=s_node, action=action, g=g, time=s_node.time + step_time)
        if g > max_g:
            max_g = g
            plan = result
        # TODO: if node.state not in closed_list:
        open_list.append(result)
        closed_list.append(result.state)
        expanded.append(result)
    return max_g, plan


if __name__ == '__main__':
    import argparse
    import agent
    import random
    import problem
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("horizon")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = problem.to_problem(x, y, int(args.max_food))
    food_dist = problem.chance_of_food(initial_state, harvester_world)
    initial_state = problem.sample(initial_state, food_dist, harvester_world)
    plan, max_g = search(initial_state, dimensions=harvester_world, horizon=int(args.horizon), return_plan=True)
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "horizon: {0}".format(args.horizon)
    print "max_g: {0}".format(max_g)
    print(plan)
    print problem.print_grid(initial_state.grid, harvester_world)
    random.seed(0)