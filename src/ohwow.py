'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
from world import *
from problem import *
def ohwow(known, prior=None): #TODO: Prior is uniform and handled by world module for now
    '''
    Agent should keep track of what it knows and send to ohwow
    '''
    n = 100 #What is a good sample size?
    horizion=2 #TODO: What should manage horizon?
    cost = -1 #Assume all actions cost the same? Makes C(s,a) irrelevant
    possible_worlds = [];
    for i in range(n):
        w = sample(4,4,known,1) #TODO: Magic numbers are size of world
        possible_worlds.append(w) 
    argmina = None #Hold action with max value
    Action = namedtuple('Action',['order','expected_reward']) #TODO: Label "order" comes from the problem. What is a more general name?
    
    #For each action applicable in s
    current_state=(1, 0)#TODO: For development only one starting state
    actions = applicable_actions1({current_state:'H'}, 4, 4) #TODO: More magic numbers representing the known world
        #Transition to next state
    max_action=None
    max_q=0 #TODO: Does 0 work?
    for action in actions:
        c = 0
        #Loop over all w in sample
        for w in possible_worlds:
            s=to_grid(w,4,4) #TODO: Magic numbers are size of world
            s_prime=transition1(current_state,action,s) 
            c += search(to_dict(s_prime),horizion) 
        q = c/float(n) #- cost
        if q > max_q:
            max_q=q
            max_action=action
    return (max_action, max_q)

if __name__ == '__main__':
    known = problem.parse('-H--\n---B')
    print(known)
    print(ohwow(known))
    #Run ohwow a bunch of times to get next action and print each new state    
