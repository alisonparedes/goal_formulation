'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
from world import *
def ohwow(known, prior=None): #TODO: Prior is uniform and handled by world module for now
    '''
    Agent should keep track of what it knows and send to ohwow
    '''
    n = 100 #What is a good sample size?
    horizion=2 #TODO: What should manage horizon?
    cost = -1 #Assume all actions cost the same? Makes C(s,a) irrelevant
    possible_worlds = [];
    for i in range(n):
        w = sample(4,4,known,1)
        possible_worlds.append(w) 
    argmina = None #Hold action with max value
    Action = namedtuple('Action',['order','expected_reward']) #TODO: Label "order" comes from the problem. What is a more general name?
    
    #For each action applicable in s
        #Transition to next state
    c = 0
    #Loop over all w in sample
    for w in possible_worlds:
        c += search(w,horizion) 
    q = c/float(n) #- cost
    return q#'N' #Return action with highest reward

if __name__ == '__main__':
    known = problem.parse('-H--\n---B')
    print(known)
    print(ohwow(known))
    #Run ohwow a bunch of times to get next action and print each new state    