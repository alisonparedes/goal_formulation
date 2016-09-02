'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple

def search(initial_state, goal_state):
    
    Node = namedtuple('Node',['state','previous','action']) #What kind of programming paradigm are factories? This is a little weird
    i = Node(initial_state, previous=None, action=None) #Are attributes implemented as copies or pointers?
    goal = Node(goal_state, previous=None, action=None)
    open_list = []
    open_list.append(i)
    closed_list = [] #TODO: Use a hash table. How would I build a hash table? and hash function?
    
    for s in open_list:
        #print(open_list) #Is it helpful to see how the open list changes?
        if is_goal(s,goal):
            return get_plan(s)    
        expanded = expand(s, Node)
        add_open(open_list, closed_list, expanded)
    return None #goal not found

def add_open(open_list, closed_list, expanded): #Lists must be mutable
    for node in expanded:
        if node.state not in closed_list:
            open_list.append(node)
            closed_list.append(node.state)

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
    pass