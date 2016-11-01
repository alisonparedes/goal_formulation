'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
import world
import problem
def ohwow(belief_state, problem_spec): #TODO: Prior is uniform and handled by world module for now
    '''
    Agent should keep track of what it knows and send to ohwow
    '''
    n = 10 #What is a good sample size?
    horizion=2 #TODO: What should manage horizon?
    cost = -1 #Assume all actions cost the same? Makes C(s,a) irrelevant
    problem_dist = problem.problem_distribution(belief_state, problem_spec)
    possible_worlds = sample(belief_state, problem_dist, n)
    #argmina = None #Hold action with max value
    #Action = namedtuple('Action',['order','expected_reward'])
    #For each action applicable in s
    actions_in_s = applicable_actions(belief_state, problem_spec)
        #Transition to next state
    max_action=None
    max_q=0 #TODO: Does 0 work?
    for action in actions_in_s: #TODO: Should be for each s_prime, not action
        c = 0
        for world in possible_worlds: #TODO: Oops. I may have broken oh-wow.
            s_prime = transition(world, action, problem_spec)
            c += search(s_prime,horizion)
        q = c/float(n) #- cost
        if q > max_q:
            max_q=q
            max_action=action
    return (max_action, max_q)

def applicable_actions(belief_state, problem_spec):
    return problem.applicable_actions(belief_state, problem_spec)#TODO: Pass a problem definition instead

def transition(belief_state, action, problem_spec):
    s_prime = problem.transition(belief_state, action, problem_spec) #TODO: Should not return integer units
    s_prime_dict=s_prime.state_dict
    return s_prime_dict

def sample(belief_state, problem_dist, n):
    possible_worlds=[]
    for i in range(n):
        w = world.sample(problem_dist,belief_state,1) 
        possible_worlds.append(w) 
    return possible_worlds

if __name__ == '__main__':
    pass
