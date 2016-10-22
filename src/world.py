'''
Created on Jul 13, 2016

@author: lenovo
'''
from copy import copy
import random
from problem import * #TODO: World and problem should maybe be in the same module

def sample(problem_distribution_arr, state, n): #TODO: When can a sample conflict with the real-world? Enabling real-world to spawn new things and the agent to imagine possible worlds where new things have spawned where it has been before. Defer to problem!
    '''
    Expects a array of probability distributions determined by the problem.
    
    N is the number of times.
    
    Assumptions:

    A seed could help debug these functions but I don't think it can be used to debug search since search
    needs to speculate about different models. 
    '''
    new_state = copy(state)
    for i in range(n):
        cell = sample_cell(problem_distribution_arr)
        coordinate=cell[1] #TODO: Use named tuples
        if coordinate:
            unit=cell[2]
            if coordinate in new_state:
                new_state[coordinate]=merge(new_state[coordinate],unit) 
            else:
                new_state[coordinate]=unit
        i += 1
    return new_state

def merge(unit_a, unit_b):
    if unit_a=='H' and unit_b=='F':
        return 'f'
    return unit_b
       
def sample_cell(problem_distribution_arr): 
    p = random.random()
    cummulative = 0
    i=-1
    while cummulative < p: #TODO: How might a recursive walk function work?
        i += 1
        cell = problem_distribution_arr[i]
        probability=cell[0] #TODO: Use named tuples
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
    