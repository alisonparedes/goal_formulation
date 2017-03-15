'''
Created on Oct 25, 2016

@author: lenovo
'''
import problem
import copy


def applicable_actions(state):

    actions = []

    harvester, _ = state.harvester_dict.iteritems().next()

    for food, _ in state.food_dict.iteritems():
        if harvester != food:
            actions.append((food, False))
            #actions.append((food, True))

    base, _ = state.base_dict.iteritems().next()
    if harvester != base:
        actions.append((base, False))
        #actions.append((base, True))

    return actions


def transition(state, action, world, time_left=1, horizon=1):

    destination, move_defender_too = action

    harvester, _ = state.harvester_dict.iteritems().next()

    new_harvester_dict = copy.copy(state.harvester_dict)
    new_food_dict = copy.copy(state.food_dict)
    new_explored_dict = copy.copy(state.explored_dict)
    new_has_food = state.has_food
    new_reward = state.reward
    new_defender_dict = copy.copy(state.defender_dict)
    new_enemy_dict = copy.copy(state.enemy_dict)
    remaining_food = copy.copy(state.future_food)

    destination_policy = None
    for goal, policy in state.distances:
        if goal == destination:
            destination_policy = policy
            break

    _, distance = destination_policy[harvester]

    if distance > time_left:
        next_step, _ = destination_policy[harvester]
        step_count = 1
        while step_count < time_left:
            next_step, _ = destination_policy[next_step]
            step_count += 1
            destination = next_step
            distance = step_count
            #for goal, policy in state.distances:
            #    if goal == destination:
            #        destination_policy = policy
            #        break


    if len(state.enemy_dict) > 0:
        enemy, _ = state.enemy_dict.iteritems().next()
        new_enemy = enemy
        next_step, distance = destination_policy[harvester]
        step_count = 0
        enemy_step = enemy
        while distance > 0:
            next_step, = destination_policy[next_step]
            step_count += 1
            destination = next_step
            distance = step_count
            enemy_policy = None
            for goal, policy in state.distances:
                if goal == next_step:
                    enemy_policy = policy
                    break
            enemy_step, = enemy_policy[enemy_step]
            if enemy_step in state.defender_dict:
                new_enemy = enemy_step
                destination = next_step
                break
            elif enemy_step == next_step:
                new_enemy = enemy_step
                destination = next_step
                break


    del new_harvester_dict[harvester]
    new_harvester_dict[destination] = 'H'
    #new_explored_dict[harvester] = '-'

    if move_defender_too:
        if len(state.defender_dict) > 0:
            defender, _ = state.defender_dict.iteritems().next()
            del new_defender_dict[defender]
        new_defender_dict[destination] = 'D'
        new_reward -= 10
        #new_explored_dict[defender] = '-'

    if len(state.enemy_dict) > 0:
        enemy, _ = state.enemy_dict.iteritems().next()
        del new_enemy_dict[enemy]
        new_enemy_dict[new_enemy] = 'E'

        if destination in new_enemy_dict:
            new_reward -= 10

    if state.has_food and destination in state.base_dict:
        new_reward += 50 * pow(0.95, horizon - time_left + distance)
        new_has_food = False

    if not state.has_food and destination in state.food_dict:
        del new_food_dict[destination]
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
                    break

    new_reward -= distance

    next_state = problem.to_state(state.base_dict,
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

    return next_state, distance


if __name__ == '__main__':
    import argparse
    import agent
    import random
    random.seed(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state")
    parser.add_argument("max_food")
    parser.add_argument("destination_x")
    parser.add_argument("destination_y")
    parser.add_argument("defender_too")
    parser.add_argument("time_left")
    args = parser.parse_args()
    initial_state, x, y = agent.init_belief(args.initial_state)
    world = problem.to_problem(x, y, int(args.max_food))
    initial_state = problem.sample(initial_state, world)
    defender_too = False
    if args.defender_too == 'True':
        defender_too = True
    next_state, action_cost = transition(initial_state, ((int(args.destination_x), int(args.destination_y)), defender_too), world, int(args.time_left), int(args.time_left))
    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "action: ({0}, {1}) defender? {2}".format(args.destination_x, args.destination_y, args.defender_too)
    print "action cost: {0}".format(action_cost)
    print "reward: {0}".format(next_state.reward)
    print(problem.print_grid(initial_state, world))
    print(problem.print_grid(next_state, world))