'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
import world
import problem

'''
Oh wow expects an incomplete state, a belief state. It maybe tuned to change sample size, search horizon, and
underlying distribution of possible worlds.
'''


def ohwow(belief_state, problem_spec, State, n=1, horizon=1):

    # Tunable parameters
    problem_dist = problem.chance_of_food(belief_state, problem_spec, chance=True)
    print(problem_dist)

    # Sample worlds
    possible_worlds = sample(belief_state.grid, problem_dist, n)
    #print 'food: {0}'.format(summarize_sample(possible_worlds, problem_spec))
    #argmina = None #Hold action with max value
    #Action = namedtuple('Action',['order','expected_reward'])
    #For each action applicable in s

    # Simulate each action available in the current world
    actions_in_s = problem.applicable_actions(belief_state.grid, problem_spec)

    max_action=None
    max_q=0
    for action in actions_in_s: #TODO: Should be for each s_prime, not action
        c = 0.0
        for world in possible_worlds:
            #print world
            #print 'has food:', belief_state.has_food

            # Simulate taking each action
            s_prime = transition(State(world, belief_state.reward, belief_state.has_food), action, problem_spec, State)
            c += s_prime.reward

            # Search from this next state
            c += search(s_prime, horizon, State)

        q = c/float(n)
        #print '{0} {1}'.format(action, q)
        if q > max_q:
            max_q=q
            max_action=action
    return max_action, max_q


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


def transition(belief_state, action, problem_spec, State):
    s_prime = problem.transition(belief_state, action, problem_spec, State) #TODO: Should not return integer units
    return s_prime.state

def sample(belief_state, problem_dist, n):
    possible_worlds=[]
    for i in range(n):
        w = world.sample(problem_dist,belief_state, max_food=2) #TODO: This magic number is in two places. Fix this ASAP.
        possible_worlds.append(w) 
    return possible_worlds

if __name__ == '__main__':
    pass
