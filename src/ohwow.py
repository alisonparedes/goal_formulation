'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
def ohwow():
    #What is known?
    #What is prior?
    n = 100.0 #What is a good sample size? 1 for testing. 
    #Sample from W
    argmina = None #Hold action with max value
    #For each action applicable in s
        #Transition to next state
    cost = -1 #Assume all actions cost the same? Makes C(s,a) irrelevant
    #Loop over all w in sample
    c = 0
    next_state = '-H--\nF--B' #For development only
    w = problem.parse(next_state)
    c += search(w,2) #For each w find c
    q = c/n #- cost
    return q#'N' #Return action with highest reward

if __name__ == '__main__':
    print(ohwow())