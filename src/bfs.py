'''
Created on Sep 1, 2016

@author: lenovo
'''
from collections import namedtuple

def search(initial_state, goal_state):
    
    Node = namedtuple('Node',['state','previous']) #TODO: Add actions. What kind of programming paradigm are factories?
    i = Node(initial_state,None)
    goal = Node(goal_state, None)
    open_list = []
    open_list.append(i)
    closed_list = []
    
    for s in open_list:
        print(open_list)
        if is_goal(s,goal):
            return get_plan(s)    
    #else expand state, e.g. add new states to queue (do not add duplicates) 
        open_list.extend(expand(s, Node))
    return None #goal not found

def is_goal(s, goal):
    if s.state == goal.state:
        return True
    return False

def get_plan(s): #TODO: Return a  list of actions; this is sequence of states
    i = s
    plan = []
    while i:
        plan.insert(0, i.state)
        i = i.previous
    return plan

def expand(s, Node): #Kind of like passing a function 
    return [Node(2,s)]

def get_actions(s):
    return []

def transition(s, action):
    return s

if __name__ == '__main__':
    print(search(1,2))
    pass