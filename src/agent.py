'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

from simulator import *
from ohwow import *
from copy import deepcopy
import os

def new_knowledge(old_world, new_world): 
    
    #TODO: Fix comparison
    #[['H', None, 'F', None], [None, None, None, None], ['H', None, None, None], [None, 'B', None, None]]
    #[['H', None, 'F', None], [None, 'H', None, None], ['H', None, None, None], [None, 'B', None, None]]
    new_knowledge={}
    x=0
    for col in new_world:
        y=0
        for cell in col:
            if old_world[x][y]!=new_world[x][y]: #TODO: Problem should provide comparison
                new_knowledge[(x,y)]=cell
            y+=1
        x+=1
    return new_knowledge
        
def new_state(state, new_knowledge):
    #TODO: Test with {(2, 0): None, (1, 0): 'H'}
    #TODO: I'd rather not copy dictionaries around. Why not modify in place? Worry about this when changing state representation per Wheeler's recommendation
    for coordinate, cell in new_knowledge.iteritems():
        if cell:
            state[coordinate]=cell 
        else:
            if coordinate in state:
                del state[coordinate]
    return state #TODO: It may be time to replace the dictionary representation? {(1, 0): 'H', (3, 1): 'B', (0, 0): None}

def get_current_state(state):
    for coordinate, cell in state.iteritems():
        if cell in 'H$*':
            return {coordinate:cell}
    return None

if __name__ == '__main__':
    real_world=[[None, None, 'F', None], ['H', None, None, None], [None, None, None, None], [None, 'B', None, None]]
    state={(1, 0): 'H', (3, 1): 'B'}
    #known= {(2, 0): None, (1, 0): 'H'}
    #print(new_state(state, known))
    while True: #TODO: True may be a bit much. When to stop?
        current_state=get_current_state(state)
        action = ohwow(current_state, state)
        old_world=deepcopy(real_world)
        new_world = simulate(state, action[0], real_world) #Modifies world 
        known=new_knowledge(old_world, new_world)
        state=new_state(state, known)
        real_world = new_world
        os.system('clear') 
        print(interleaved(state, real_world)) #TODO: Swap these parameters to reflect order states will be printed
