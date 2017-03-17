'''
Created on Sep 28, 2016

@author: Alison Paredes
'''

import problem
from collections import namedtuple
import copy



def simulate(belief_state, action, real_world, dimensions):
    """
    Decides what agent can see
    """
    # print("Simulator:")
    # print(real_world.future_food)
    new_state, observations = problem.transition(real_world, action, dimensions)

    new_observation_food = {}
    new_observation_enemy = {}
    hypothetical_food_dict = copy.copy(belief_state.food_dict)

    if observations.food:
        for food, add_delete in observations.food.iteritems():
            if food in belief_state.food_dict and add_delete == -1:
                new_observation_food[food] = add_delete
                del hypothetical_food_dict[food]
            elif food in new_state.harvester_dict and add_delete == 1:
                new_observation_food[food] = add_delete
                hypothetical_food_dict[food] = 'F'
            elif len(hypothetical_food_dict) < 1 and dimensions.max_food >= 2:
                new_observation_food[food] = add_delete
                hypothetical_food_dict[food] = 'F'
            elif dimensions.known:
                new_observation_food[food] = add_delete

    if observations.enemy:
        for enemy, add_delete in observations.enemy.iteritems():
            if enemy in belief_state.enemy_dict and add_delete == -1:
                new_observation_enemy[enemy] = add_delete
            elif add_delete == 1:
                enemy_x, enemy_y = enemy
                if (enemy_x + 1, enemy_y) in new_state.harvester_dict\
                    or (enemy_x + 1, enemy_y) in new_state.defender_dict\
                    or (enemy_x - 1, enemy_y) in new_state.harvester_dict\
                    or (enemy_x - 1, enemy_y) in new_state.defender_dict\
                    or (enemy_x, enemy_y + 1) in new_state.harvester_dict\
                    or (enemy_x, enemy_y + 1) in new_state.defender_dict\
                    or (enemy_x, enemy_y - 1) in new_state.harvester_dict\
                    or (enemy_x, enemy_y - 1) in new_state.defender_dict:
                    new_observation_enemy[enemy] = add_delete
            elif dimensions.known:
                new_observation_enemy[enemy] = add_delete

    #print(new_state.enemy_dict)

    new_observations = problem.to_observation(obstacle=observations.obstacle,
                                              harvester=observations.harvester,
                                              food=new_observation_food,
                                              defender=observations.defender,
                                              enemy=new_observation_enemy,
                                              reward=observations.reward,
                                              has_food=observations.has_food,
                                              step_reward=observations.reward - belief_state.reward)


    return new_state, new_observations


if __name__ == '__main__':
    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("action")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    harvester_world = problem.to_problem(x, y, int(args.max_food))
    food_dist = problem.chance_of_food(initial_state, harvester_world)
    initial_state = problem.sample(initial_state, food_dist, harvester_world)
    next_state, observations = simulate(initial_state, args.action, initial_state, harvester_world)
    belief_state = agent.update_belief(initial_state, observations)
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "action: {0}".format(args.action)
    print "reward: {0}".format(next_state.reward)
    print(problem.interleaved(initial_state.grid, next_state.grid, harvester_world))
    random.seed(0)
