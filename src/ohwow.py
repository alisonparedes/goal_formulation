'''
Created on Sep 21, 2016

@author: Alison Paredes
'''
from bfs_g import *
import world
import problem
def ohwow(belief_state, problem_spec, State): #TODO: Prior is uniform and handled by world module for now
    '''
    Ohwow expects a belief state which is an object of type State and usually incomplete.

    A belief state should contain a
    dictionary of coordinates locating objects in the world. It should know if the agent has food or not. It should
    know how much reward has been earned so far.

    Ohwow returns an action and its expected value.
    '''

    # Tunable parameters
    n = 10
    horizon = 10

    max_action = None
    max_q=-1000
    actions_in_s = applicable_actions(belief_state.state, problem_spec)
    # TODO: Applicable actions should accept a state object and parse out what it needs, e.g. coordinates.

    # Sample possible worlds
    problem_dist = problem.problem_distribution(belief_state.state, problem_spec)
    possible_worlds = sample(belief_state.state, problem_dist, n)
    # TODO: Sample should accept a state object and return a state object as long as it doesn't slow us down.
    print 'food frequency: {0}'.format(summarize_sample(possible_worlds, problem_spec))

    for action in actions_in_s:
        # TODO: Should be for each next state, not action but each action, but for OK for now.
        c = -1000.0
        for world in possible_worlds:
            print 'world:', world
            print 'action: ', action
            s = State(world, belief_state.reward, belief_state.has_food)
            s_next = transition(s, action, problem_spec, State)
            # TODO: Maybe get the reward from this step and add it to c?
            print 'next state:', s_next
            c += search(s_next, horizon, State)
            print '\n'
        q = c/float(n) #- cost
        print 'action: {0} {1}'.format(action, q)
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
    '''

    :param belief_state:
    :param action:
    :param problem_spec:
    :param State:
    :return:
    '''
    s_prime = problem.transition(belief_state, action, problem_spec, State)
    return s_prime

def sample(belief_state, problem_dist, n):
    possible_worlds=[]
    for i in range(n):
        w = world.sample(problem_dist,belief_state, max_food=2) #TODO: This magic number is in two places. Fix this ASAP.
        possible_worlds.append(w) 
    return possible_worlds

if __name__ == '__main__':
    pass
