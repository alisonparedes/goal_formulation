'''
Created on Sep 3, 2015

@author: Alison
'''

from collections import deque
import problem
from copy import deepcopy
  
def dijkstra(goal, problem): #TODO: Run to a horizon, i.e. number of nodes expanded
    #TODO: Initialize open list
    
    open_list = deque([goal])
    policy = empty_policy(problem) #TODO: What is this if it isn't a policy? =
    policy[goal[0]][goal[1]]='B' #TODO: How to separate this logic from dijkstra?
    while len(open_list) > 0:  #TODO: Instead of goal state run to horizon, i.e. run n times
        explored = open_list.popleft()     
        expand(explored, open_list, policy, problem)
    return policy #Always returns something, since there is no goal state, only a reward

def expand(current_state, open_list, policy, problem):
    for action in actions(current_state, problem): #Actions are directions
        next_state=transition(current_state,action,problem)
        x=next_state[0]
        y=next_state[1]
        if policy[x][y] == None:       
            open_list.append(next_state) #States are coordinates
            policy[x][y]=current_state
        
        
def actions(state, problem):
    w=len(problem)
    h=len(problem[0])
    actions=[]
    x=state[0]
    y=state[1]
    if x+1 < w:
        actions.append((1,0))
    if x-1 >= 0:
        actions.append((-1,0))
    if y+1 < h: 
        actions.append((0,1))
    if y-1 >= 0:
        actions.append((0,-1))
    return actions

def empty_policy(problem):
    w=len(problem)
    h=len(problem[0])
    grid = []
    for i in range(w): #TODO: I don't need i.
        grid.append([None]*h) #Meh
    return grid

def transition(state, action, problem):
    next_x=state[0]+action[0]
    next_y=state[1]+action[1]
    return (next_x,next_y)


        
if __name__ == '__main__':
    problem=[['H', None, 'F', None], [None, None, None, None], ['H', None, None, None], [None, 'B', None, None]]
    goal=(3,1)
    print(dijkstra(goal, problem))
    