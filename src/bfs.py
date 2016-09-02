'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple

def search(initial_state, goal_state, horizon=float("inf")): 
    
    Node = namedtuple('Node',['state','previous','action']) #What kind of programming paradigm are factories? This is a little weird
    i = Node(initial_state, previous=None, action=None) #Are attributes implemented as copies or pointers?
    goal = Node(goal_state, previous=None, action=None)
    
    open_list = [i]
    closed_list = [] #TODO: Use a hash table. How would I build a hash table? and hash function?
    depth = 0 #TODO: Is there a good way to encapsulate depth
    current_level = 1
    next_level = 0
    while len(open_list) > 0 and depth <= horizon:
        s = open_list.pop(0)
        current_level -= 1
        if is_goal(s,goal):
            return get_plan(s)    
        expanded = expand(s, Node)
        next_level += add_open(open_list, closed_list, expanded)
        if current_level == 0:
            current_level = next_level
            next_level = 0
            depth += 1
    return get_plan(s) #goal not found

def add_open(open_list, closed_list, expanded): #Lists must be mutable
    appended = 0
    for node in expanded:
        if node.state not in closed_list: #Tested by commenting "+ action" out of transition function for now
            open_list.append(node)
            closed_list.append(node.state)
            appended += 1
    return appended

def is_goal(s, goal):
    if equals(s, goal): 
        return True
    return False

def get_plan(s): 
    i = s
    plan = []
    while i.previous:
        plan.insert(0, i.action)
        i = i.previous
    return plan

def expand(s, Node): #Kind of like passing a function? 
    expanded=[]
    for action in applicable_actions(s):
        result = Node(state=transition(s, action),previous=s,action=action) #Is this going to be a problem?
        expanded.append(result)
    return expanded

def applicable_actions(s): #TODO: Pass a function from the problem
    return [1]

def transition(s, action):
    return s.state + action #TODO: Pass a function from the problem

def equals(s1, s2):
    return s1.state == s2.state #TODO: Pass comparator for problem as a function

if __name__ == '__main__':
    print(1 <= float("inf"))
    pass