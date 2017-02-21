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
    parser.add_argument("file_name")
    args = parser.parse_args()

    random.seed(1)

    dimensions = problem.to_problem(int(args.width), int(args.width))

    for i in range(int(args.n_worlds)):
        grid = {}
        b_x, b_y = random_coordinate(int(args.width), int(args.height))
        grid[(b_x, b_y)] = "b"

        for _ in range(int(args.max_food)):
            x, y = random_coordinate(int(args.width), int(args.height))
            grid[(x, y)] = "F"

            with open("../test/{0}_{1}.world".format(args.file_name, i), "w") as world_file:
                world_file.write(problem.print_grid(grid, dimensions))


