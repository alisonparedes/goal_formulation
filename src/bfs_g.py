'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple, deque
import problem

def search(initial_state, horizon=float("inf")):  #TODO: Get rid of goal test completely? For NRL scenario, scores, not goals, determine success.
    
    Node = namedtuple('Node',['state','previous','action', 'g']) #What kind of programming paradigm are factories a part of? 
    State = namedtuple('State',['state','value']) #TODO: Problem should handle state structure.
    Expanded = namedtuple('Expanded',['len','max_g'])
    Simulated = namedtuple('Simulated',['state','resources'])
    i = Node(State(initial_state,0), previous=None, action=None, g=0) #TODO: How to delegate creating an initial State object to problem?
    #goal = Node(State(goal_state,0), previous=None, action=None, g=None) #g is N/A for goal test
    
    open_list = deque([i])
    closed_list = deque([]) #TODO: Use a hash table. How would I build a hash table? and hash function? Can Python hash a dictionary?
    depth = 0 #TODO: Is there a good way to encapsulate depth test?
    current_level = 1 
    next_level = 0
    nodes_generated = 1
    nodes_expanded = 0
    max_g = 0
    while len(open_list) > 0 and depth < horizon:
        s = open_list.popleft() 
        #print(s.state)
        current_level -= 1
        #if is_goal(s,goal): #TODO: Take out goal test. Goal test is N/A
        #    return get_plan(s)    
        expanded = expand(s, Node, open_list, closed_list, max_g, State, Expanded, Simulated) 
        #A bunch of counts
        nodes_expanded+=1
        next_level += expanded.len #add_open(open_list, closed_list, expanded) #Checking closed list as each node is expanded instead
        nodes_generated += expanded.len
        max_g = expanded.max_g
        if current_level == 0: #TODO: Encapsulate!
            current_level = next_level
            next_level = 0
            depth += 1
            #print(current_level)
    print(nodes_generated)
    print(nodes_expanded)
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

def expand(s, Node, open_list, closed_list, max_g, State, Expanded, Simulated): #Kind of like passing a function? 
    expanded=[]
    for action in applicable_actions(s): 
        next_state = transition(s, action, State, Simulated) #TODO: Transition should return value of next_state
        g=next_state.value #TODO: Delegate g of value of next state from current state and next state. Search should only use g.
        max_g = max(max_g,g)
        result = Node(state=next_state, previous=s, action=action, g=g) #Are tuple factories going to be a problem? TODO: Calculate g as we go. G is over sequence + current. Currently assumes all actions cost -1
        #if node.state not in closed_list: #TODO: What if a state were represented by a dictionary of positions and objects? Encapsulate this to delegate comparison to problem module.
        open_list.append(result)
        closed_list.append(result.state)
        expanded.append(result)
    return Expanded(len(expanded),max_g)

def applicable_actions(s): #TODO: Pass a function from the problem
    return problem.applicable_actions(s.state)

def transition(s_node, action, State, Simulated):
    next_state=problem.transition(s_node.state, action, State, Simulated)
    return next_state#TODO: Problem figures out how to modify the dictionary

def equals(s1, s2):
    return s1.state == s2.state #TODO: N/A if removing goal test

if __name__ == '__main__':
    simstate = '-H--\nF--B'
    initial_state = problem.parse(simstate)
    goal_state = 10
    max_g=search(initial_state,goal_state,2)
    print(max_g)