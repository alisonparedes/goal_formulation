'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import simulator
from ohwow import *
from copy import deepcopy
import os

#TODO: I dont' think agent should ahve access to old_world vsy7. new_world, especially since the real_world should be able to change in ways that the agent doesn't know about, e.g. spawn new food. Simulator could return new_world and percept.
def new_knowledge(old_world, new_world, current_state): #TODO: When should an agent remove an attribute from his belief state? Never? World sample could speculate about visited states. When is belief state this fluid? Fluents are allowed to change over time.
    
    new_knowledge={}
    x=0
    for col in new_world:
        y=0
        for cell in col:
            if old_world[x][y]!=new_world[x][y]: #TODO: Problem should provide comparison
                new_knowledge[(x,y)]=cell
            y+=1
        x+=1
    new_knowledge=merge_history(current_state, new_knowledge) #TODO: Hmm...new_knowledge should have been modified in place
    return new_knowledge

def merge_history(current_state, new_knowledge): #TODO: There must be a function to merge two dictionaries. 
    for coordinate, cell in current_state.iteritems(): 
        if cell in 'H':
            new_knowledge[coordinate]='-'
    return new_knowledge
        
def new_state(state, new_knowledge):
    for coordinate, cell in new_knowledge.iteritems():
        if cell:
            state[coordinate]=cell 
        else:
            if coordinate in state:
                del state[coordinate]
    return state #TODO: It may be time to replace the dictionary representation? {(1, 0): 'H', (3, 1): 'B', (0, 0): None}

def get_current_state(state):
    for coordinate, cell in state.iteritems():
        if cell in 'H$*!0':
            return {coordinate:cell}
    return None

if __name__ == '__main__': #TODO: What arguments should it accept?
    real_world=[[None, None, 'F', None], ['H', None, None, None], [None, None, None, None], [None, 'B', None, None]]
    belief_state={(1, 0): 'H', (3, 1): 'B'}
    problem_spec=(len(real_world), len(real_world[0]))
    print(problem_spec)
    while True: #TODO: True may be a bit much. When to stop?
        current_state = get_current_state(belief_state) #TODO: Why not use just belief state?
        action = ohwow(current_state, belief_state)
        old_world = deepcopy(real_world) #TODO: Why not modify in place?
        new_world = simulator.simulate(belief_state, action[0], real_world) #Modifies world 
        known = new_knowledge(old_world, new_world, current_state) #TODO: Maybe simulator needs to return new observations
        belief_state = new_state(belief_state, known)
        real_world = new_world
        os.system('clear') 
        print(problem.interleaved(belief_state, real_world)) #TODO: Swap these parameters to reflect order states will be printed
