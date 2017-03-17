import problem;

def random_coordinate(width, height):
    x = random.randint(0, width  - 1)
    y = random.randint(0, height - 1)
    return x, y

if __name__ == '__main__':
    import argparse
    import random
    import problem

    parser = argparse.ArgumentParser()
    parser.add_argument("width")
    parser.add_argument("height")
    parser.add_argument("max_food")
    parser.add_argument("n_worlds")
    parser.add_argument("n_obstacles")
    parser.add_argument("enemy")
    parser.add_argument("scenario")
    parser.add_argument("file_name")
    args = parser.parse_args()

    random.seed(1)

    dimensions = problem.to_problem(int(args.width), int(args.width))

    for w in range(int(args.n_worlds)):
        harvester_dict = {}
        food_dict = {}
        defender_dict = {}
        enemy_dict = {}
        obstacle_dict = {}
        base_dict = {}
        belief_food_dict = {}

        b_x, b_y = random_coordinate(int(args.width), int(args.height))
        base_dict[(b_x, b_y)] = "b"
        harvester_dict[(b_x, b_y)] = "b"

        i = 0
        while i < int(args.max_food):
            x, y = random_coordinate(int(args.width), int(args.height))
            if (x, y) not in base_dict:
                food_dict[(x, y)] = "F"
                if int(args.scenario) == 1 and len(belief_food_dict) == 0:
                    belief_food_dict[(x, y)] = 'F'
                i += 1

        i = 0
        while i < int(args.n_obstacles):
            x, y = random_coordinate(int(args.width), int(args.height))
            if (x, y) not in base_dict \
                    and (x, y) not in food_dict:
                obstacle_dict[(x, y)] = '#'
                i += 1

        i = 0
        while i < int(args.enemy):
            x, y = random_coordinate(int(args.width), int(args.height))
            if (x, y) not in base_dict \
                    and (x, y) not in food_dict\
                    and (x, y not in obstacle_dict):
                enemy_dict[(x, y)] = 'E'
                i += 1

        belief = problem.to_state(base_dict,
                                  harvester_dict,
                                  food=belief_food_dict)

        reality = problem.to_state(base_dict,
                                   harvester_dict,
                                   food=food_dict,
                                   obstacle=obstacle_dict,
                                   enemy=enemy_dict)

        with open("../test/{0}_{1}_real.world".format(args.file_name, w), "w") as world_file:
            world_file.write(problem.state_to_string(reality, dimensions))
        with open("../test/{0}_{1}_belief.world".format(args.file_name, w), "w") as world_file:
            world_file.write(problem.state_to_string(belief, dimensions))


