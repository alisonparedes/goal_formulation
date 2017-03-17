'''
Created on Aug 18, 2016

@author: lenovo
'''
import random
import copy

from collections import namedtuple
from copy import deepcopy  # I am not sure if copy would have been sufficient
import dijkstra


def to_problem(x, y, max_food=0, known=False, enemy=False):
    Problem = namedtuple("Problem", ["x", "y", "max_food", "known", "enemy"])
    return Problem(x, y, max_food, known, enemy)


def to_state(base,
             harvester,
             food=None,
             obstacle=None,
             defender=None,
             enemy=None,
             explored=None,
             has_food=False,
             reward=0,
             future_food=[],
             distances={},
             step_reward=0):
    State = namedtuple('State', ['base_dict',
                                 'harvester_dict',
                                 'food_dict',
                                 'obstacle_dict',
                                 'defender_dict',
                                 'enemy_dict',
                                 'explored_dict',
                                 'has_food',
                                 'reward',
                                 'future_food',
                                 'distances',
                                 'step_reward'])
    if not explored:
        explored = {}
    if not defender:
        defender = {}
    if not obstacle:
        obstacle = {}
    if not food:
        food = {}
    if not enemy:
        enemy = {}
    return State(base,
                 harvester,
                 food,
                 obstacle,
                 defender,
                 enemy,
                 explored,
                 has_food,
                 reward,
                 future_food,
                 distances,
                 step_reward)


def to_observation(obstacle=None, harvester=None, food=None, defender=None, enemy=None, reward=0, has_food=False, step_reward=0):
    Observation = namedtuple("Observation", ["obstacle",
                                             "harvester",
                                             "food",
                                             "defender",
                                             "enemy",
                                             "reward",
                                             "has_food",
                                             "step_reward"])
    return Observation(obstacle, harvester, food, defender, enemy, reward, has_food, step_reward)


def parse(simstate):
    base = {}
    harvester = {}
    food = {}
    obstacle = {}
    defender = {}
    enemy = {}
    has_food = False
    y = 0
    x = 0
    for cell in simstate:

        if cell == 'b':
            harvester[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == 'H':
            harvester[(x, y)] = cell

        elif cell == 'B':
            base[(x, y)] = cell

        elif cell == 'F':
            food[(x, y)] = cell

        elif cell == '$':
            harvester[(x, y)] = cell
            #food[(x, y)] = cell
            has_food = True

        elif cell == '*':
            harvester[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == '#':
            obstacle[(x, y)] = cell

        elif cell == 'D':
            defender[(x, y)] = cell

        elif cell == 'd':
            harvester[(x, y)] = cell
            defender[(x, y)] = cell
            #base[(x, y)] = cell

        elif cell == 'E':
            enemy[(x, y)] = cell

        elif cell == '!':
            harvester[(x, y)] = cell
            enemy[(x, y)] = cell

        elif cell == '0':
            harvester[(x, y)] = cell
            enemy[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == '1':
            enemy[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == '2':
            defender[(x, y)] = cell
            base[(x, y)] = cell

        elif cell == '3':
            enemy[(x, y)] = cell
            harvester[(x, y)] = cell
            has_food = True

        elif cell == '4':
            food[(x, y)] = cell
            harvester[(x, y)] = cell
            has_food = True


        elif cell == '\n':
            y += 1
            x =- 1 #Hmm...
        x += 1    
    return base, harvester, food, obstacle, defender, enemy, has_food


def interleaved(reality, belief, world, known=True):
    reality_grid = to_ascii_array(reality, world)
    belief_grid = to_ascii_array(belief, world, known)
    printable = ''
    for y in range(world.y):
        for x in range(world.x):
            printable += reality_grid[x][y]
        printable += ' '
        for x in range(world.x):
            printable += belief_grid[x][y]
        printable += '\n'
    return printable


def to_ascii_array(state, world, known=True):
    default_char = '-'
    if not known:
        default_char = '?'
    state_grid = [[default_char for _ in range(world.y)] for _ in range(world.x)]

    for explored, _ in state.explored_dict.iteritems():
        explored_x, explored_y = explored
        state_grid[explored_x][explored_y] = '-'

    for obstacle, _ in state.obstacle_dict.iteritems():
        obstacle_x, obstacle_y = obstacle
        state_grid[obstacle_x][obstacle_y] = '#'

    for food, _ in state.food_dict.iteritems():
        food_x, food_y = food
        state_grid[food_x][food_y] = 'F'

    for base, _ in state.base_dict.iteritems():
        base_x, base_y = base
        state_grid[base_x][base_y] = 'B'

    harvester, _ = state.harvester_dict.iteritems().next()
    harvester_x, harvester_y = harvester
    if harvester in state.base_dict:
        if state.has_food:
            state_grid[harvester_x][harvester_y] = '*'
        else:
            state_grid[harvester_x][harvester_y] = 'b'
    elif state.has_food:
        state_grid[harvester_x][harvester_y] = '$'
    elif harvester in state.food_dict:
        state_grid[harvester_x][harvester_y] = 'f'
    else:
        state_grid[harvester_x][harvester_y] = 'H'

    defender_item = next(state.defender_dict.iteritems(), None)
    if defender_item:
        defender, _ = defender_item
        defender_x, defender_y = defender
        if defender in state.harvester_dict:
            state_grid[defender_x][defender_y] = 'd'
        else:
            state_grid[defender_x][defender_y] = 'D'

    enemy_item = next(state.enemy_dict.iteritems(), None)
    if enemy_item:
        enemy, _ = enemy_item
        enemy_x, enemy_y = enemy
        if enemy in state.harvester_dict:
            state_grid[enemy_x][enemy_y] = '!'
        else:
            state_grid[enemy_x][enemy_y] = 'E'

    return state_grid


def state_to_string(state, world):
    state_grid = to_ascii_array(state, world)
    printable = ''
    for y in range(world.y):
        for x in range(world.x):
            printable += state_grid[x][y]
        printable += '\n'
    return printable


def basic_actions(start, state, problem, enemy=False):
    actions = []
    x, y = start
    if y-1 >= 0 and ((x, y-1) not in state.obstacle_dict):
        if not enemy or (x, y-1) not in state.defender_dict:
            actions.append('N')
    if y+1 < problem.y and ((x, y+1) not in state.obstacle_dict):
        if not enemy or (x, y+1) not in state.defender_dict:
            actions.append('S')
    if x+1 < problem.x and ((x+1, y) not in state.obstacle_dict):
        if not enemy or (x+1, y) not in state.defender_dict:
            actions.append('E')
    if x-1 >= 0 and ((x-1, y) not in state.obstacle_dict):
        if not enemy or (x-1, y) not in state.defender_dict:
            actions.append('W')
    return actions


def applicable_actions(state, problem):
    actions = []
    harvester, _ = state.harvester_dict.iteritems().next()
    x, y = harvester
    if y-1 >= 0 and ((x, y-1) not in state.obstacle_dict):
        actions.append('N')
        actions.append('ND')
    if y+1 < problem.y and ((x, y+1) not in state.obstacle_dict):
        actions.append('S')
        actions.append('SD')
    if x+1 < problem.x and ((x+1, y) not in state.obstacle_dict):
        actions.append('E')
        actions.append('ED')
    if x-1 >= 0 and ((x-1, y) not in state.obstacle_dict):
        actions.append('W')
        actions.append('WD')
    return actions


def transition(state, action, world):

    move_harvester_in_direction = action[0]
    move_defender_too = False
    if len(action) > 1 and action[1] == 'D':
        move_defender_too = True

    harvester, _ = state.harvester_dict.iteritems().next()
    new_x, new_y = harvester

    if move_harvester_in_direction == 'N':
        new_y -= 1
        if new_y < 0:
            return state, None
    elif move_harvester_in_direction == 'S':
        new_y += 1
        if new_y >= world.y:
            return state, None
    elif move_harvester_in_direction == 'E':
        new_x += 1
        if new_x >= world.x:
            return state, None
    elif move_harvester_in_direction == 'W':
        new_x -= 1
        if new_x < 0:
            return state, None

    if (new_x, new_y) in state.obstacle_dict:
        return state, to_observation(obstacle={(new_x, new_y): 1}, reward=state.reward - 1)

    new_harvester_dict = copy.copy(state.harvester_dict)
    new_food_dict = copy.copy(state.food_dict)
    new_explored_dict = copy.copy(state.explored_dict)
    new_has_food = state.has_food
    new_reward = state.reward
    new_defender_dict = copy.copy(state.defender_dict)
    new_enemy_dict = copy.copy(state.enemy_dict)
    remaining_food = copy.copy(state.future_food)

    observation_harvester_dict = {}
    observation_explored_dict = {}
    observation_food_dict = {}
    observation_defender_dict = {}
    observation_enemy_dict = {}

    del new_harvester_dict[harvester]
    new_harvester_dict[(new_x, new_y)] = 'H'
    observation_harvester_dict[(new_x, new_y)] = 1
    new_explored_dict[harvester] = '-'
    observation_harvester_dict[harvester] = -1
    observation_explored_dict[harvester] = 1
    new_reward -= 1

    if move_defender_too:
        if len(state.defender_dict) > 0:
            defender, _ = state.defender_dict.iteritems().next()
            del new_defender_dict[defender]
            observation_defender_dict[defender] = -1
        new_defender_dict[(new_x, new_y)] = 'D'
        observation_defender_dict[(new_x, new_y)] = 1
        new_reward -= 1
        #new_explored_dict[defender] = '-'

    if len(state.enemy_dict) > 0:
        enemy, _ = state.enemy_dict.iteritems().next()
        #for goal, policy in state.distances:
        #    if goal == (new_x, new_y):
        #        new_enemy_x_y, _ = policy[enemy]
        policy = dijkstra.dijkstra((new_x, new_y), state, world, enemy=True)
        if enemy in policy:
            new_enemy_x_y, _ = policy[enemy]
            if new_enemy_x_y == '*':
                new_enemy_x_y = (new_x, new_y)
            if new_enemy_x_y not in new_defender_dict:
                del new_enemy_dict[enemy]
                new_enemy_dict[new_enemy_x_y] = 'E'
                observation_enemy_dict[enemy] = -1
                observation_enemy_dict[new_enemy_x_y] = 1
                #new_reward -= 10
            else:
                new_enemy_x, new_enemy_y = new_enemy_x_y
                if new_enemy_x + 1 < world.x and (new_enemy_x + 1, new_enemy_y) not in state.obstacle_dict:
                    del new_enemy_dict[enemy]
                    observation_enemy_dict[enemy] = -1
                    new_enemy_dict[(new_enemy_x + 1, new_enemy_y)] = 'E'
                    observation_enemy_dict[(new_enemy_x + 1, new_enemy_y)] = 1

                elif new_enemy_x - 1 >= 0 and (new_enemy_x - 1, new_enemy_y) not in state.obstacle_dict:
                    del new_enemy_dict[enemy]
                    observation_enemy_dict[enemy] = -1
                    new_enemy_dict[(new_enemy_x - 1, new_enemy_y)] = 'E'
                    observation_enemy_dict[(new_enemy_x - 1, new_enemy_y)] = 1

                elif new_enemy_y + 1 < world.y and (new_enemy_x, new_enemy_y + 1) not in state.obstacle_dict:
                    del new_enemy_dict[enemy]
                    observation_enemy_dict[enemy] = -1
                    new_enemy_dict[(new_enemy_x, new_enemy_y + 1)] = 'E'
                    observation_enemy_dict[(new_enemy_x, new_enemy_y + 1)] = 1

                elif new_enemy_y - 1 >= 0 and (new_enemy_x, new_enemy_y - 1) not in state.obstacle_dict:
                    del new_enemy_dict[enemy]
                    observation_enemy_dict[enemy] = -1
                    new_enemy_dict[(new_enemy_x, new_enemy_y - 1)] = 'E'
                    observation_enemy_dict[(new_enemy_x, new_enemy_y - 1)] = 1

        if (new_x, new_y) in new_enemy_dict:
            new_reward -= 10

    if state.has_food and (new_x, new_y) in state.base_dict:
        new_reward += 50
        new_has_food = False

    if (new_x, new_y) in state.food_dict:
        if state.has_food:
            observation_food_dict[(new_x, new_y)] = 1
        else:
            del new_food_dict[(new_x, new_y)]
            observation_food_dict[(new_x, new_y)] = -1
            new_has_food = True
            new_explored_dict = {}
            while len(new_food_dict) < world.max_food:
                while True:
                    try_x = remaining_food.pop()
                    try_y = remaining_food.pop()
                    remaining_food.insert(0, try_x)
                    remaining_food.insert(0, try_y)
                    try_coordinate = (try_x, try_y)
                    if try_coordinate not in state.base_dict \
                            and try_coordinate not in state.obstacle_dict \
                            and try_coordinate not in new_harvester_dict \
                            and try_coordinate not in new_explored_dict:
                        new_food_dict[try_coordinate] = 'F'
                        #if world.known:
                        observation_food_dict[try_coordinate] = 1
                        break


    next_state = to_state(state.base_dict,
                          new_harvester_dict,
                          food=new_food_dict,
                          obstacle=state.obstacle_dict,
                          defender=new_defender_dict,
                          explored=new_explored_dict,
                          enemy=new_enemy_dict,
                          has_food=new_has_food,
                          reward=new_reward,
                          future_food=remaining_food,
                          distances=state.distances)


    observations = to_observation(obstacle=None,
                                  harvester=observation_harvester_dict,
                                  food=observation_food_dict,
                                  defender=observation_defender_dict,
                                  enemy=observation_enemy_dict,
                                  reward=new_reward,
                                  has_food=new_has_food)
    return next_state, observations


def sample(belief_state, dimensions):
    """Constructs a world from a belief state"""
    new_food_dict = sample_max_food(belief_state, dimensions)
    new_enemy_dict = copy.copy(belief_state.enemy_dict)
    if dimensions.enemy:
        new_enemy_dict = sample_enemy(belief_state, dimensions)
    if dimensions.known:
        future_food = belief_state.future_food
    else:
        future_food = sample_n_future_food(dimensions, 100)
    distances = all_distances(belief_state, dimensions)
    complete_state = to_state(belief_state.base_dict,
                              belief_state.harvester_dict,
                              food= new_food_dict,
                              obstacle=belief_state.obstacle_dict,
                              defender=belief_state.defender_dict,
                              enemy=new_enemy_dict,
                              explored=belief_state.explored_dict,
                              has_food=belief_state.has_food,
                              reward=belief_state.reward,
                              distances=distances,
                              future_food=future_food)
    return complete_state


def all_distances(state, problem):
    distances = []
    for x in range(problem.x):
        for y in range(problem.y):
            if (x, y) not in state.obstacle_dict:
                distances.append(((x, y), dijkstra.dijkstra((x, y), state, problem)))
    return distances


def adjacent_coordinate(coordinate, action):
    x = y = 0
    if action == 'N':
        y = -1
    elif action == 'S':
        y = 1
    elif action == 'E':
        x = 1
    elif action == 'W':
        x = -1
    next_x = coordinate[0] + x
    next_y = coordinate[1] + y
    return next_x, next_y


def to_dict(w):
    state={}
    x=0
    for col in w:
        y=0
        for cell in col:
            if cell:
                state[(x,y)]=cell
            y+=1
        x+=1
    return state


def sample_cell(width, height):
    sampled_x = random.randint(0, width - 1)
    sampled_y = random.randint(0, height - 1)
    return sampled_x, sampled_y


def sample_max_food(state, dimensions):

    #print(grid)
    new_food_dict = deepcopy(state.food_dict)
    while len(new_food_dict) < dimensions.max_food:
        #print(try_coordinate)
        try_coordinate = sample_cell(dimensions.x, dimensions.y)
        if try_coordinate not in state.base_dict \
                and try_coordinate not in state.obstacle_dict \
                and try_coordinate not in state.harvester_dict \
                and try_coordinate not in state.explored_dict:
            new_food_dict[try_coordinate] = 'F'
    return new_food_dict

def sample_enemy(state, dimensions):

    #print(grid)
    new_enemy_dict = deepcopy(state.enemy_dict)
    while len(new_enemy_dict) < 1:
        #print(try_coordinate)
        try_coordinate = sample_cell(dimensions.x, dimensions.y)
        if try_coordinate not in state.base_dict \
                and try_coordinate not in state.obstacle_dict \
                and try_coordinate not in state.harvester_dict \
                and try_coordinate not in state.explored_dict:
            new_enemy_dict[try_coordinate] = 'E'
    return new_enemy_dict



def sample_n_future_food(harvester_world, n=1):
    food_sequence = []
    for _ in range(n):
        food_sequence.append(random.randint(0, harvester_world.x - 1))
    return food_sequence


if __name__ == '__main__':
    import argparse
    import agent

    random.seed(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("action")
    args = parser.parse_args()

    initial_state, x, y = agent.init_belief(args.initial_state)
    world = to_problem(x, y, int(args.max_food))

    # complete_state = sample_max_food(initial_state, harvester_world)
    distances = all_distances(initial_state, world)
    future_food = sample_n_future_food(world, 100)
    initial_state = to_state(initial_state.base_dict,
                             initial_state.harvester_dict,
                             food=initial_state.food_dict,
                             obstacle=initial_state.obstacle_dict,
                             defender=initial_state.defender_dict,
                             enemy=initial_state.enemy_dict,
                             explored=initial_state.explored_dict,
                             has_food=initial_state.has_food,
                             reward=initial_state.reward,
                             distances=distances,
                             future_food=future_food)
    # initial_state = sample(initial_state, harvester_world)

    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "action: {0}".format(args.action)

    next_state, observations = transition(initial_state, args.action, world)

    print(state_to_string(initial_state, world))
    print(state_to_string(next_state, world))
    print "reward: {0}".format(next_state.reward)
    print "has_food: {0}".format(next_state.has_food)
    print "observation: {0}".format(observations)
    #print(observations)


    
