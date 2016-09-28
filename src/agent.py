'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

from simulator import *
from ohwow import *

def new_knowledge(old_world, new_world):
    
    new_knowledge={}
    x=0
    for col in old_world:
        y=0
        for cell in col:
            if old_world[x][y]!=new_world[x][y]: #TODO: Problem should provide comparison
                new_knowledge[(x,y)]=cell
            y+=1
        x+=1
    return new_knowledge
        
def new_state(state, new_knowledge):
    for coordinate, cell in new_knowledge:
        state[coordinate]=cell 
    return state


if __name__ == '__main__':
    real_world=[[None, None, 'F', None], ['H', None, None, None], [None, None, None, None], [None, 'B', None, None]]
    state={(1, 0): 'H', (3, 1): 'B'}
    while True: #TODO: True may be a bit much. When to stop?
        action = ohwow(state)
        new_world = simulate(state, action, real_world)
        know=new_knowledge(real_world, new_world)
        state=new_state(state, know)
        real_world = new_world
