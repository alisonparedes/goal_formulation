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
    i = to_node(initial_state, previous=None, action=None, g=0, time=0)
    #goal = Node(State(goal_state,0), previous=None, action=None, g=None) #g is N/A for goal test
    open_list = deque([i])
    closed_list = deque([])  # TODO: Use a hash table. How would I build a hash table? and hash function? Can Python hash a dictionary?
    current_level = 1
    nodes_expanded = 0
    max_g = 0
    plan = None
    time = 0

    while len(open_list) > 0 and time < horizon: #depth < horizon:

        s = open_list.popleft()

        #print(s.state)
        current_level -= 1
        # if is_goal(s,goal):
        #    return get_plan(s)    
        max_g, plan, time = expand(s, open_list, closed_list, max_g, dimensions)
        nodes_expanded += 1

    #print(nodes_generated)
    #print(nodes_expanded)
    if return_plan:
        print 'plan:', get_plan(plan), max_g
    return max_g #Return highest reward, not plan


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


def expand(s_node, open_list, closed_list, max_g, dimensions):
    expanded = []
    plan = s_node
    time = s_node.time
    for action in relaxed_problem.applicable_actions(s_node.state):
        next_state, time = relaxed_problem.transition(s_node.state, action, dimensions)
        g = next_state.reward
        result = to_node(state=next_state, previous=s_node, action=action, g=g, time=time)
        if g > max_g:
            max_g = g
            plan = result
        # TODO: if node.state not in closed_list:
        open_list.append(result)
        closed_list.append(result.state)
        expanded.append(result)
    return max_g, plan, time


if __name__ == '__main__':
    pass