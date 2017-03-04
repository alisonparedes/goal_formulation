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
    parser.add_argument("file_name")
    args = parser.parse_args()

    random.seed(1)

    dimensions = problem.to_problem(int(args.width), int(args.width))

    for w in range(int(args.n_worlds)):
        reality = {}
        belief = {}
        b_x, b_y = random_coordinate(int(args.width), int(args.height))
        reality[(b_x, b_y)] = "b"
        belief[(b_x, b_y)] = "b"

        i = 0
        while i < int(args.max_food):
            x, y = random_coordinate(int(args.width), int(args.height))
            if (x, y) not in reality:
                reality[(x, y)] = "F"
                i += 1

        i = 0
        while i < int(args.n_obstacles):
            x, y = random_coordinate(int(args.width), int(args.height))
            if (x, y) not in reality:
                reality[(x, y)] = '#'
                i += 1

        with open("../test/{0}_{1}_real.world".format(args.file_name, w), "w") as world_file:
            world_file.write(problem.print_grid(reality, dimensions))
        with open("../test/{0}_{1}_belief.world".format(args.file_name, w), "w") as world_file:
            world_file.write(problem.print_grid(belief, dimensions))


