'''
Created on Jul 13, 2016

@author: lenovo
'''
from copy import copy
import random

def sample(w, h, known, n):
    '''
    Expects a dictionary describing the known state of the world, the size of the map and probability distribution of the world
    '''
        
    map = copy(known)
    i = copy(n)      #TODO: Replace i with a probability distribution. Why make a copy?
    while i > 0: #How unusual is this way of doing something n times? Scary if i is a reference, maybe.
        location = random_loc(w, h)
        thing = random_thing() #Sample shouldn't conflict with known state of the world
        map[location]=thing #TODO: Changed map to dict. How does it affect other functions in world.py
        i-=1
    return map
       

def random_loc(w, h):
    x = random.randint(0, w-1)
    y = random.randint(0, h-1)
    return (x, y)   
    

def random_thing():
    things = ['E','F'] #TODO: Consider moving this logic (or the entier sampling function to problem)
    r = random.randint(0,len(things)-1)
    return things[r]
    

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

if __name__ == '__main__':
    known = [[(1,1),'@']]
    m = sample(10, 10, known, 10)
    print_r(m)
    