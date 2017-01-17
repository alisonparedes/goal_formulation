'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple, deque
import relaxed_problem


'''
Returns total reward
'''


def search(initial_state, horizon, distances, State, return_plan=False):  #TODO: Get rid of goal test completely? For NRL scenario, scores, not goals, determine success.
    
    Node = namedtuple('Node',['state','previous','action', 'g','t']) #What kind of programming paradigm are factories a part of?
    Expanded = namedtuple('Expanded',['len','max_g','plan','t'])

    i = Node(initial_state, previous=None, action=None, g=0, t=0) #TODO: How to delegate creating an initial State object to problem?
    #goal = Node(State(goal_state,0), previous=None, action=None, g=None) #g is N/A for goal test

    open_list = deque([i])
    closed_list = deque([]) #TODO: Use a hash table. How would I build a hash table? and hash function? Can Python hash a dictionary?
    depth = 0 #TODO: Is there a good way to encapsulate depth test?
    current_level = 1 
    next_level = 0
    nodes_generated = 1
    nodes_expanded = 0
    max_g = 0
    plan = None
    time = 0

    while len(open_list) > 0 and time < horizon: #depth < horizon:

        s = open_list.popleft()

        #print(s.state)
        current_level -= 1
        #if is_goal(s,goal):
        #    return get_plan(s)    
        expanded = expand(s, Node, open_list, closed_list, max_g, distances, State, Expanded, horizon)
        nodes_expanded+=1
        next_level += expanded.len #add_open(open_list, closed_list, expanded) #Checking closed list as each node is expanded instead
        nodes_generated += expanded.len
        max_g = expanded.max_g
        time = expanded.t

        if expanded.plan:
            plan = expanded.plan

        if current_level == 0:
            current_level = next_level
            next_level = 0
            depth += 1
            #print(current_level)

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
    HEAD=0 
    i = s
    plan = []
    while i.previous:
        plan.insert(HEAD, i.action)
        i = i.previous
    return plan

def expand(s, Node, open_list, closed_list, max_g, distances, State, Expanded, horizon):
    expanded=[]
    plan=None
    t=0
    for action in applicable_actions(s):
        next_state = transition(s, action, distances, State, horizon) #TODO: Transition should return value of next_state
        g=next_state.reward #TODO: Delegate g of value of next state from current state and next state. Search should only use g.
        t=next_state.t
        result = Node(state=next_state, previous=s, action=action, g=g, t=t) #Are tuple factories going to be a problem? TODO: Calculate g as we go. G is over sequence + current. Currently assumes all actions cost -1
        if g > max_g:
            max_g = g
            plan=result
        #if node.state not in closed_list: #TODO: What if a state were represented by a dictionary of positions and objects? Encapsulate this to delegate comparison to problem module.
        open_list.append(result)
        closed_list.append(result.state)
        expanded.append(result)
    return Expanded(len(expanded),max_g, plan, t)

def applicable_actions(s): #TODO: Pass a function from the problem
    return relaxed_problem.applicable_actions(s.state)

def transition(s_node, action, distances, State, horizon):
    next_state = relaxed_problem.transition(s_node.state, action, distances, State, horizon)
    return next_state

def equals(s1, s2):
    return s1.state == s2.state #TODO: N/A if removing goal test

if __name__ == '__main__':
    pass