from problem import *
from ohwow import *

if __name__ == '__main__':
    simstate = '-H\n-B'
    grid = parse(simstate)
    State = namedtuple('State',['grid','has_food'])
    state = State(grid, has_food = True)
    print(state)
    problem_spec=(2,2)
    distribution = chance_of_food(state, problem_spec)
    print(distribution)
    possible_worlds = sample(state.grid, distribution, 1000)
    print 'food: {0}'.format(summarize_sample(possible_worlds, problem_spec))