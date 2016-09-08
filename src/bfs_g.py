'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple
import problem

def search(initial_state, goal_state, horizon=float("inf")):  #TODO: Get rid of goal test completely? For NRL scenario, scores, not goals, determine success.
    
    Node = namedtuple('Node',['state','previous','action', 'g']) #What kind of programming paradigm are factories a part of? 
    i = Node(initial_state, previous=None, action=None, g=0) #g could trend positive or negative and noop is an option
    goal = Node(goal_state, previous=None, action=None, g=None) #g is N/A for goal test
    
    open_list = [i]
    closed_list = [] #TODO: Use a hash table. How would I build a hash table? and hash function? Can Python hash a dictionary?
    depth = 0 #TODO: Is there a good way to encapsulate depth test?
    current_level = 1 
    next_level = 0
    nodes_generated = 1
    nodes_expanded = 0
    while len(open_list) > 0 and depth < horizon:
        s = open_list.pop(0)
        print(s.state)
        current_level -= 1
        #if is_goal(s,goal): #TODO: Take out goal test. Goal test is N/A
        #    return get_plan(s)    
        expanded = expand(s, Node, open_list, closed_list) #TODO: Is Python copying lists around?
        #A bunch of counts
        nodes_expanded+=1
        next_level += len(expanded) #add_open(open_list, closed_list, expanded) #Checking closed list as each node is expanded instead
        nodes_generated += len(expanded)
        if current_level == 0: #TODO: Encapsulate!
            current_level = next_level
            next_level = 0
            depth += 1
            #print(current_level)
    print(nodes_generated)
    print(nodes_expanded)
    return get_plan(min_g(open_list)) #goal not found return best on open instead

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

def is_goal(s, goal):
    if equals(s, goal): 
        return True
    return False

def min_g(open_list): #TODO: Returns the best looking node on the open list.
    return open_list[0] #TODO: Right now returns the first node on open. Sort on g. Watch this. Sorting half of all nodes ever generated could be slow! Maybe sort g as nodes are generated? Is g an accurate variable name since in addition to action cost it considers next state's reward? Since it isn't an estimate of cost to go (h) then in contrast g I think using g is OK.

def get_plan(s):
    HEAD=0 
    i = s
    plan = []
    while i.previous:
        plan.insert(HEAD, i.action)
        i = i.previous
    return plan

def expand(s, Node, open_list, closed_list): #Kind of like passing a function? 
    expanded=[]
    for action in applicable_actions(s): 
        result = Node(state=transition(s, action), previous=s, action=action, g=s.g-1) #Are tuple factories going to be a problem? TODO: Calculate g as we go. G is over sequence + current. Currently assumes all actions cost -1
        #if node.state not in closed_list: #TODO: What if a state were represented by a dictionary of positions and objects? Encapsulate this to delegate comparison to problem module.
        open_list.append(result)
        closed_list.append(result.state)
        expanded.append(result)
    return expanded

def applicable_actions(s): #TODO: Pass a function from the problem
    return problem.applicable_actions(s.state)

def transition(s, action):
    return problem.transition(s.state, action) #TODO: Problem figures out how to modify the dictionary

def equals(s1, s2):
    return s1.state == s2.state #TODO: N/A if removing goal test

if __name__ == '__main__':
    pass