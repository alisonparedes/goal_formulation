'''
Created on Jul 13, 2016

@author: lenovo
'''
from copy import copy
import random
from problem import * #TODO: World and problem should maybe be in the same module

def sample(problem_distribution_arr, grid, maxfood=1):
    '''
    Expects a 2D array of probability distributions determined by the problem. 
    Example [(0.5,(0,1),'F'),(0.5,None)]
    
    N is the number of new cells to sample.
    
    Assumptions:

    A seed could help debug these functions but I don't think it can be used to debug search since search
    needs to speculate about different models. 
    '''
    new_grid = copy(grid)
    while count_food(new_grid) < maxfood:
        x = sample_cell(problem_distribution_arr)
        update_state(new_grid, x)
    return new_grid

def count_food(grid):
    food = 0
    for coordinate, unit in grid.iteritems():
        if unit == 'F':
            food += 1
    return food

def update_state(state, sample): #Modifies state in place
    coordinate=sample[1]
    if coordinate:
        unit=sample[2]
        if coordinate in state:
            state[coordinate]=merge(state[coordinate],unit) 
        else:
            state[coordinate]=unit

def merge(unit_a, unit_b):
    if unit_a in 'b$*H' and unit_b in 'F':
        return '$'
    if unit_a in '$' and unit_b in 'B':
        return '*'
    if unit_a in 'H' and unit_b in 'B':
        return 'b'
    if unit_a in 'b*':
        return 'H'
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


if __name__ == '__main__':
    pass
