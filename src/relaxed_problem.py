'''
Created on Oct 25, 2016

@author: lenovo
'''
import math

def applicable_actions(s): #TODO: Units (or combinations of units, e.g. fleet) takes actions so state model needs to provide quick access to units' positions.  Although if world is small enough iterating through dictionary of positions may not be that big of a problem, .e.g one harvester and one base.
    '''
    Returns an iterable list of actions applicable in the given state.
    '''
    actions=[]
    units=''
    food_coordinates=[]
    for coordinate, unit in s.state.iteritems():
        if unit in 'F':
            food_coordinates.append(coordinate)
        if unit in 'HBF$*@':
            units+=unit
    if ('H' in units or '$' in units ) and ('B' in units):
        actions.append('HB')
    if ('H' in units or '*' in units) and ('F' in units): #TODO: How could this work passing funcitons?
        for food_coordinate in food_coordinates:
            actions.append('HF' + '_' + str(food_coordinate[0]) + '_' + str(food_coordinate[1]))
    '''if ('*' in units or '$' in units or '!' in units) and '@' in units:
        actions.append('HS')'''
    return actions
    #return [1,2]
    
def transition(state, action_and_coordinate, State): #TODO: Assumes action is valid
    '''
    Returns the next state (s') and its value(?) from the current state (s) given an action. 
    '''
    action = action_and_coordinate.split('_')[0]
    next_state=None
    if action == 'HB':
        next_state=hb(state, State) #TODO: I'm not sure I like passing class specifications (what are these exactly?) around but it seems like it should belong to functional programming
    elif action == 'HF':
        coordinate = (int(action_and_coordinate.split('_')[1]), int(action_and_coordinate.split('_')[2]))
        next_state=hf(state, coordinate, State)
    return next_state
    #return s

def hb(state, State):
    '''
    Simulate moving harvester to base
    '''
    new_map = {}
    from_coordinate=()
    to_coordinate=()
    for coordinate, unit in state.state.iteritems():
        if unit == 'H':
            #next_state[coordinate]='@' #Start
            from_coordinate=coordinate
        elif unit in '$': #TODO: Top level planners may need to use the same symbols
            #next_state[coordinate]=None #Never restock
            from_coordinate=coordinate
        elif unit == 'B':
            new_map[coordinate]='*'
            to_coordinate=coordinate
        else:
            new_map[coordinate]=unit #TODO: Too much iterating!
    resources = distance(from_coordinate, to_coordinate)
    has_food = state.has_food
    if has_food:
        has_food = False
    new_reward = state.reward
    next_state = State(new_map,new_reward, has_food)
    new_reward += reward(next_state) - resources
    return State(new_map,new_reward, has_food)

def distance(from_coordinate, to_coordinate):
    from_x=float(from_coordinate[0])
    from_y=float(from_coordinate[1])
    to_x=float(to_coordinate[0])
    to_y=float(to_coordinate[1])
    distance=math.sqrt(math.pow(from_x - to_x,2) + math.pow(from_y - to_y,2))
    return distance * 10

def hf(state, food_coordinate, State):
    '''
    Simulate moving harvester to food
    '''
    new_map = {}
    from_coordinate=()
    to_coordinate=()
    for coordinate, unit in state.state.iteritems():
        if unit == 'H':
            #next_state[coordinate]='@' #Start
            from_coordinate=coordinate
        elif unit == 'F' and coordinate == food_coordinate :
            new_map[coordinate]='$' #Food fully stocked
            to_coordinate=coordinate
        elif unit in '*':
            new_map[coordinate]='B' #Been home once already
            from_coordinate=coordinate
        else:
            new_map[coordinate]=unit
    resources = distance(from_coordinate, to_coordinate)
    has_food = True
    new_reward = state.reward
    next_state = State(new_map, new_reward, has_food)
    new_reward += reward(next_state) - resources
    return next_state
    
def reward(s): #Expecting State object
    reward=0
    for coordinate, unit in s.state.iteritems(): #TODO: How much is this slowing my BFS down?
        if unit in '*':
            reward+=100 #State tracks if base has ever been visited before
            if s.has_food:
                reward += 50
    return reward

if __name__ == '__main__':
    pass