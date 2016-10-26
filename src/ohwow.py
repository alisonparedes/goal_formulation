'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
import world
import problem
def ohwow(current_state, belief_state, prior=None): #TODO: Prior is uniform and handled by world module for now
    '''
    Agent should keep track of what it knows and send to ohwow
    '''
    n = 100 #What is a good sample size?
    horizion=2 #TODO: What should manage horizon?
    cost = -1 #Assume all actions cost the same? Makes C(s,a) irrelevant
    problem_dist = [(0.066, (0, 0), 'F'), (0.066, (0, 1), 'F'), (0.066, (0, 2), 'F'), (0.066, (0, 3), 'F'), (0.066, (1, 0), 'F'), (0.066, (1, 1), 'F'), (0.066, (1, 2), 'F'), (0.066, (1, 3), 'F'), (0.066, (2, 0), 'F'), (0.066, (2, 1), 'F'), (0.066, (2, 2), 'F'), (0.066, (2, 3), 'F'), (0.066, (3, 0), 'F'), (0.066, (3, 1), 'F'), (0.066, (3, 2), 'F'), (0.066, (3, 3), 'F')]
    possible_worlds = sample(belief_state, problem_dist, n)
    #argmina = None #Hold action with max value
    #Action = namedtuple('Action',['order','expected_reward']) #TODO: Label "order" comes from the problem. What is a more general name?
    #For each action applicable in s
    actions_in_s = applicable_actions(belief_state) 
        #Transition to next state
    max_action=None
    max_q=0 #TODO: Does 0 work?
    for action in actions_in_s:
        c = 0
        #Loop over all w in sample
        for world in possible_worlds:
            s_prime = transition(belief_state, action)
            c += search(s_prime,horizion) 
        q = c/float(n) #- cost
        if q > max_q:
            max_q=q
            max_action=action
    return (max_action, max_q)

def applicable_actions(belief_state):
    return problem.applicable_actions(belief_state, 4, 4)#TODO: Pass a problem definition instead

def transition(belief_state, action):
    s_prime_dict=problem.transition(belief_state, action) #TODO: Should not return integer units
    return s_prime_dict

def sample(belief_state, problem_dist, n):
    possible_worlds=[]
    for i in range(n):
        w = world.sample(problem_dist,belief_state,1) 
        possible_worlds.append(w) 
    return possible_worlds

if __name__ == '__main__':
    pass
