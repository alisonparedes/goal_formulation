'''
Created on Oct 25, 2016

@author: lenovo
'''
import problem
import copy
import dijkstra


def applicable_actions(state):

    actions = []

    harvester, _ = state.harvester_dict.iteritems().next()

    for food, _ in state.food_dict.iteritems():
        if harvester != food:
            actions.append(food)

    base, _ = state.base_dict.iteritems().next()
    if harvester != base:
        actions.append(base)

    return actions


def transition(state, destination, world, time_left=1, horizon=1):
    #print(destination, time_left)
    #print(problem.state_to_string(state, world))
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
        distance = step_count
        destination = next_step
        while step_count < time_left:
            next_step, _ = destination_policy[next_step]
            step_count += 1
            destination = next_step
            distance = step_count

    deploy_defender = False
    defender, _ = state.defender_dict.iteritems().next()
    if len(state.enemy_dict) > 0:
        turn = True
        next_step, _ = destination_policy[harvester]
        step_count = 1
        turn = not turn

        enemy, _ = state.enemy_dict.iteritems().next()
        #enemy_policy = None
        #for goal, policy in state.distances:
        #    if goal == next_step:
        #        enemy_policy = policy
        #        break

        enemy_step = enemy
        #enemy_step, _ = enemy_policy[enemy_step]
        new_enemy = enemy_step  # TODO: I might not need to store the previous step any more

        while step_count < distance or not turn:

            if enemy_step == next_step:
                destination = next_step
                distance = step_count
                new_enemy = enemy_step
                deploy_defender = True
                break

            else:
                if turn:
                    next_step, _ = destination_policy[next_step]
                    step_count += 1
                    turn = not turn
                else:
                    #enemy_policy = None
                    #for goal, policy in state.distances:
                    #    if goal == next_step:
                    #        enemy_policy = policy
                    #        break
                    enemy_policy = dijkstra.dijkstra(next_step, state, world, enemy=True)
                    new_enemy = enemy_step
                    if enemy_step in enemy_policy:
                        try_enemy_step, _ = enemy_policy[enemy_step]
                        if try_enemy_step not in state.defender_dict:
                            new_enemy = try_enemy_step
                    turn = not turn

        del new_enemy_dict[enemy]
        new_enemy_dict[new_enemy] = 'E'

    del new_harvester_dict[harvester]
    new_harvester_dict[destination] = 'H'
    #new_explored_dict[harvester] = '-'

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
                remaining_food.insert(0, try_x)
                while try_x >= world.x:
                    try_x = remaining_food.pop()
                    remaining_food.insert(0, try_x)

                try_y = remaining_food.pop()
                remaining_food.insert(0, try_y)
                while try_y >= world.y:
                    try_y = remaining_food.pop()
                    remaining_food.insert(0, try_y)

                try_coordinate = (try_x, try_y)
                if try_coordinate not in state.base_dict \
                        and try_coordinate not in state.obstacle_dict \
                        and try_coordinate not in new_harvester_dict \
                        and try_coordinate not in new_explored_dict:
                    new_food_dict[try_coordinate] = 'F'
                    break

    new_reward -= distance

    alt_reward = new_reward
    if deploy_defender:
        destination_x, destination_y = destination
        defender_x, defender_y = defender
        alt_reward -= 1 * (abs(destination_x - defender_x) + abs(destination_y - defender_y))

    next_state = problem.to_state(state.base_dict,
                                  new_harvester_dict,
                                  food=new_food_dict,
                                  obstacle=state.obstacle_dict,
                                  defender=state.defender_dict,
                                  explored=new_explored_dict,
                                  enemy=new_enemy_dict,
                                  has_food=new_has_food,
                                  reward=new_reward,
                                  future_food=remaining_food,
                                  distances=state.distances)

    alt_enemy_dict = copy.copy(new_enemy_dict)
    if deploy_defender:
        new_defender_dict[destination] = 'D'
        if len(state.defender_dict) > 0:
            defender, _ = state.defender_dict.iteritems().next()
            del new_defender_dict[defender]
        alt_reward -= 10
        if new_enemy in new_defender_dict:
            new_enemy_x, new_enemy_y = new_enemy
            if new_enemy_x + 1 < world.x and (new_enemy_x + 1, new_enemy_y) not in state.obstacle_dict:
                del alt_enemy_dict[new_enemy]
                #observation_enemy_dict[enemy] = -1
                alt_enemy_dict[(new_enemy_x + 1, new_enemy_y)] = 'E'
                #observation_enemy_dict[(new_enemy_x + 1, new_enemy_y)] = 1

            elif new_enemy_x - 1 >= 0 and (new_enemy_x - 1, new_enemy_y) not in state.obstacle_dict:
                del alt_enemy_dict[new_enemy]
                #observation_enemy_dict[enemy] = -1
                alt_enemy_dict[(new_enemy_x - 1, new_enemy_y)] = 'E'
                #observation_enemy_dict[(new_enemy_x - 1, new_enemy_y)] = 1

            elif new_enemy_y + 1 < world.y and (new_enemy_x, new_enemy_y + 1) not in state.obstacle_dict:
                del alt_enemy_dict[new_enemy]
                #observation_enemy_dict[enemy] = -1
                alt_enemy_dict[(new_enemy_x, new_enemy_y + 1)] = 'E'
                #observation_enemy_dict[(new_enemy_x, new_enemy_y + 1)] = 1

            elif new_enemy_y - 1 >= 0 and (new_enemy_x, new_enemy_y - 1) not in state.obstacle_dict:
                del alt_enemy_dict[new_enemy]
                #observation_enemy_dict[enemy] = -1
                alt_enemy_dict[(new_enemy_x, new_enemy_y - 1)] = 'E'
                #observation_enemy_dict[(new_enemy_x, new_enemy_y - 1)] = 1

    alt_state = problem.to_state(state.base_dict,
                                 new_harvester_dict,
                                 food=new_food_dict,
                                 obstacle=state.obstacle_dict,
                                 defender=new_defender_dict,
                                 explored=new_explored_dict,
                                 enemy=alt_enemy_dict,
                                 has_food=new_has_food,
                                 reward=alt_reward,
                                 future_food=remaining_food,
                                 distances=state.distances)
    result = [(next_state, distance)]

    if deploy_defender:
        result.append((alt_state, distance))

    return result


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
    parser.add_argument("time_left")
    args = parser.parse_args()

    initial_state, x, y = agent.init_belief(args.initial_state)
    world = problem.to_problem(x, y, int(args.max_food))
    initial_state = problem.sample(initial_state, world)

    print "initial_state: {0}".format(args.initial_state)
    print "max_food: {0}".format(args.max_food)
    print "action: ({0}, {1})".format(args.destination_x, args.destination_y)

    print(initial_state)
    next_states = transition(initial_state, (int(args.destination_x), int(args.destination_y)), world, int(args.time_left), int(args.time_left))

    print(problem.state_to_string(initial_state, world))

    for next_state, action_cost in next_states:
        print(problem.state_to_string(next_state, world))

        print "action cost: {0}".format(action_cost)
        print "reward: {0}".format(next_state.reward)
        print "distance: {0}".format(action_cost)

        print(next_state)