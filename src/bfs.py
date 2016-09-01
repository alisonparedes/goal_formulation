'''
Created on Sep 1, 2016

@author: lenovo
'''

def search(initial_state, goal_state):
    #initialize queue with initial_state
    open_list = []
    open_list.append(initial_state)
    #loop for each state in queue:
    for state in open_list:
        print(open_list)
        if state == goal_state:
            return get_plan(state)    
    #else expand state, e.g. add new states to queue (do not add duplicates) 
        open_list.extend(expand(state))
    return None #goal not found

def get_plan(state): #TODO:
    return state

def expand(state):
    return [2]

if __name__ == '__main__':
    print(search(1,2))
    pass