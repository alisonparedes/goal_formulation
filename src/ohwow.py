'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
import world
import problem
def ohwow(belief_state, problem_spec, State): #TODO: Prior is uniform and handled by world module for now
    '''
    Agent should keep track of what it knows and send to ohwow
    '''
    n = 100 #What is a good sample size?
    horizion=10 #TODO: What should manage horizon?
    problem_dist = problem.problem_distribution(belief_state.state, problem_spec)
    possible_worlds = sample(belief_state.state, problem_dist, n)
    print 'food: {0}'.format(summarize_sample(possible_worlds, problem_spec))
    #argmina = None #Hold action with max value
    #Action = namedtuple('Action',['order','expected_reward'])
    #For each action applicable in s
    actions_in_s = applicable_actions(belief_state.state, problem_spec)
        #Transition to next state
    max_action=None
    max_q=-1000 #TODO: Does 0 work? Umm no
    for action in actions_in_s: #TODO: Should be for each s_prime, not action
        c = -1000.0
        for world in possible_worlds:
            print world
            print 'has food:', belief_state.has_food
            s_prime = transition(State(world,belief_state.reward,belief_state.has_food), action, problem_spec, State)
            print 's_prime:', s_prime #Maybe get the reward from this step and add it to c?
            c += search(s_prime,horizion, State)
        q = c/float(n) #- cost
        print '{0} {1}'.format(action, q)
        if q > max_q:
            max_q=q
            max_action=action
    return (max_action, max_q)


def summarize_sample(possible_worlds, problem_spec):
    summary_grid=[]
    for i in range(problem_spec[0]):
        summary_grid.append([])
        for j in range(problem_spec[1]):
            summary_grid[i].append(0)
    for world in possible_worlds:
        for coordinate, unit in world.iteritems():
            if unit in 'F':
                summary_grid[coordinate[0]][coordinate[1]] += 1
    return summary_grid



def applicable_actions(belief_state, problem_spec):
    return problem.applicable_actions(belief_state, problem_spec)#TODO: Pass a problem definition instead

def transition(belief_state, action, problem_spec, State):
    s_prime = problem.transition(belief_state, action, problem_spec, State) #TODO: Should not return integer units
    return s_prime.state_dict

def sample(belief_state, problem_dist, n):
    possible_worlds=[]
    for i in range(n):
        w = world.sample(problem_dist,belief_state, max_food=2) #TODO: This magic number is in two places. Fix this ASAP.
        possible_worlds.append(w) 
    return possible_worlds

if __name__ == '__main__':
    pass
