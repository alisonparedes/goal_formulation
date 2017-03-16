'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple, deque
import relaxed_problem
import copy
import problem


def to_node(state, previous, action, g=0, time=0, step_time=0):
    Node = namedtuple('Node', ['state', 'previous', 'action', 'g', 'time', 'step_time'])
    return Node(state, previous, action, g, time, step_time)


def search(initial_state, dimensions, horizon=1, return_plan=False):

    #print(initial_state)
    i = to_node(initial_state, previous=None, action=None, g=0, time=0, step_time=0)
    open_list = deque([i])
    closed_list = deque([])
    nodes_expanded = 0
    max_g = -1000
    plan = None
    q = 0
    while len(open_list) > 0:
        s = open_list.popleft()
        #print(q, get_plan(s))

        q += 1
        # if s.previous:
            # compare_grid(s.state.grid, s.previous.state.grid)
            # compare_g(s, s.previous)
            # compare_future(s.state, s.previous.state)
        if s.time >= horizon:
            if s.g > max_g:
                max_g = s.g
                plan = s
        else:
            expand(s, open_list, closed_list, max_g, dimensions, horizon)
            nodes_expanded += 1

    #for action, state in get_plan(plan):
    #    print("action: {0}\n".format(action))
    #    print(problem.state_to_string(state, dimensions))
    #return_plan = True
    #print(max_g, get_plan(plan))
    if return_plan:
#        return get_plan(plan), max_g
        print(max_g, get_plan(plan))
    return max_g


def compare_future(current_state, parent_state):
    current = copy.copy(current_state.future_food)
    parent = copy.copy(parent_state.future_food)
    if parent != current:
        popped = 0
        match = False
        while not match:
            popped += 1
            parent.pop()
            if parent[-10:-1] == current[-10:-1]:
                match = True
        if popped > 8:
            print(popped, "Parent:", parent[-10:-1], "Current:", current[-10:-1])
        return False
    return True


def compare_g(current_node, parent_node):
    if current_node.g - parent_node.g > 50:
        print("G:", parent_node.g, current_node.g)
        return False
    return True


def compare_grid(current_grid, parent_grid):
    diff = set(current_grid) - set(parent_grid)
    for d in diff:
        if not( parent_grid.get(d) == None and current_grid.get(d) == 'F'):
             print ("Test failed:", d, "Parent:", parent_grid.get(d), "Current:", current_grid.get(d))
             return False
    return True

'''
def add_open(open_list, closed_list, expanded): #Lists must be m utable
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
        plan.insert(HEAD, (i.action, i.g, i.time))
        i = i.previous
    return plan


def expand(s_node, open_list, closed_list, max_g, dimensions, horizon):
    expanded = []
    #@print(s_node.state)
    for action in relaxed_problem.applicable_actions(s_node.state):
        #print(action)
        next_states = relaxed_problem.transition(s_node.state, action, dimensions, horizon - s_node.time, horizon)

        for next_state, step_time in next_states:
            #if s_node.time + step_time > 10:
            #    print("hmm...", step_time, s_node.time, action, horizon, s_node.state)
            result = to_node(state=next_state, previous=s_node, action=action, g=next_state.reward, time=s_node.time + step_time, step_time=step_time)
            # if g > max_g:
            #    max_g = g
            #    plan = result
            # TODO: if node.state not in closed_list
            open_list.append(result)
            closed_list.append(result.state)
            expanded.append(result)



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