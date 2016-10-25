'''
Created on Jul 13, 2016

@author: lenovo
'''
from copy import copy
import random
from problem import * #TODO: World and problem should maybe be in the same module

def sample(problem_distribution_arr, state, n): #TODO: When can a sample conflict with the real-world? Enabling real-world to spawn new things and the agent to imagine possible worlds where new things have spawned where it has been before. Defer to problem!
    '''
    Expects a 2D array of probability distributions determined by the problem. 
    Example [(0.5,(0,1),'F'),(0.5,None)]
    
    N is the number of new cells to sample.
    
    Assumptions:

    A seed could help debug these functions but I don't think it can be used to debug search since search
    needs to speculate about different models. 
    '''
    new_state = copy(state)
    for i in range(n):
        x = sample_cell(problem_distribution_arr)
        update_state(new_state, x)
        i += 1
    return new_state

def update_state(state, sample): #Modifies state in place
    coordinate=sample[1] #TODO: Use named tuples to hold coordinate
    if coordinate:
        unit=sample[2] #TODO: Use named tuple to hold unit
        if coordinate in state:
            state[coordinate]=merge(state[coordinate],unit) 
        else:
            state[coordinate]=unit

    

def merge(unit_a, unit_b):
    if unit_a=='H' and unit_b in 'F': #TODO: Add the rest of possible F. Use problem's decoding funcitons?
        return '$'
    return unit_b
       
def sample_cell(problem_distribution_arr): #TODO: What to return when p > max of proability distribution? Should problem insure prob array sums to 1?
    p = random.random()
    cummulative = 0
    i=-1
    while cummulative < p: #TODO: How might a recursive walk function work?
        i += 1
        cell = problem_distribution_arr[i]
        probability=cell[0] #TODO: Use named tuple to hold probability
        cummulative += probability
    return cell
      
'''  
def print_r(things):
    print 'x,y,a,e,f,t'
    for thing in things:
        decoded = decode(thing[1]) #TODO: Use a named variable instead, an object (record in Ocaml?)
        print '{0},{1},{2},{3},{4},{5}'.format(thing[0][0],thing[0][1],decoded[0],decoded[1],decoded[2],decoded[3]) #TODO: OMG!


def decode(thing):
    if thing == 'E':
        return (0,1,0,0)
    if thing == 'F':
        return (0,0,1,0)
    if thing == 'T':
        return (0,0,0,1)
    if thing == '@':
        return (1,0,0,0)
'''

if __name__ == '__main__':
    pass
