'''
Created on Oct 25, 2016

@author: lenovo
'''
def applicable_actions(s): #TODO: Units (or combinations of units, e.g. fleet) takes actions so state model needs to provide quick access to units' positions.  Although if world is small enough iterating through dictionary of positions may not be that big of a problem, .e.g one harvester and one base.
    '''
    Returns an iterable list of actions applicable in the given state.
    '''
    #TODO: What is definitive list of actions? For now harvester should always have exactly two applicable actions.
    HB = 1 #move harvester to base
    HF = 2 #move harvester to food
    HS = 3 #move harvester somewhere else
    actions=[]
    units=''
    for coordinate, unit in s.state.iteritems():
        if unit in 'HBF$*@0!bf':
            units+=unit
    if ('H' in units or '$' in units or '0' in units) and ('B' in units or 'b' in units):
        actions.append(HB)
    if ('H' in units or '*' in units or '!' in units) and ('F' in units or 'f' in units):
        actions.append(HF)
    if ('*' in units or '$' in units or '0' in units or '!' in units) and '@' in units:
        actions.append(HS)
    return actions
    #return [1,2]
    
def transition(s, action, State, Simulated): #TODO: Assumes action is valid
    '''
    Returns the next state (s') and its value(?) from the current state (s) given an action. 
    '''
    if action == 1: #HB
        simulated=hb(s.state, Simulated) #TODO: I'm not sure I like passing class specifications (what are these exactly?) around but it seems like it should belong to functional programming
    elif action == 2: #HF
        simulated=hf(s.state, Simulated)
    elif action == 3: #HS
        simulated=hs(s.state, Simulated)
    resources=simulated.resources
    new_reward=s.reward + reward(s.state) - resources 
    return State(simulated.state, new_reward) #
    #return s

def hb(state, Simulated): 
    '''
    Simulate moving harvester to base
    '''
    next_state = {}
    for coordinate, unit in state.iteritems():
        if unit == 'H':
            next_state[coordinate]='@' #Start
        elif unit in '$0': #TODO: Top level planners may need to use the same symbols
            next_state[coordinate]='f' #Never restock
        elif unit == 'B':
            next_state[coordinate]='*'
        elif unit == 'b':
            next_state[coordinate]='!' #Nothing for the prodigal son?
        else:
            next_state[coordinate]=unit #TODO: Too much iterating!
    return Simulated(next_state,resources=-1)
    #return (state,-1)

def hf(state, Simulated):
    '''
    Simulate moving harvester to food
    '''
    next_state = {}
    for coordinate, unit in state.iteritems():
        if unit == 'H':
            next_state[coordinate]='@' #Start
        elif unit == 'F':
            next_state[coordinate]='$' #Food fully stocked
        elif unit == 'f':
            next_state[coordinate]='0' #No food here :(
        elif unit in '*!':
            next_state[coordinate]='b' #Been home once already 
        else:
            next_state[coordinate]=unit
    return Simulated(next_state,resources=-1)
    #return (state,-1)


def hs(state, Simulated):
    '''
    Simulate harvester somewhere else
    '''
    next_state = {}
    for coordinate, unit in state.iteritems():
        if unit == '$':
            next_state[coordinate]='f' #Never restock food (F)
        elif unit in '*!':
            next_state[coordinate]='b'
        elif unit == '@':
            next_state[coordinate]='H'
        else:
            next_state[coordinate]=unit
    return Simulated(next_state,resources=-1)
    #return (state,-1)
    
def reward(state):
    reward=0
    for coordinate, unit in state.iteritems(): #TODO: How much is this slowing my BFS down?
        if unit == '$': #State tracks when food has been depleted
            reward+=50 
        elif unit == '*':
            reward+=100 #State tracks if base has ever been visited before
    return reward

if __name__ == '__main__':
    pass