from f_utils import u_pickle
from model.grid_blocks import GridBlocks
from algo.astar import AStar


path_repo = 'd:\\temp\\write\\'
pickle_problems = path_repo + 'problems.pickle'
csv_with = path_repo + 'with.csv'
csv_without = path_repo + 'without.csv'


def create_problems():
    li = list()
    for i in range(100000):
        grid = GridBlocks(5, 5, 25)
        start, goal = grid.points_random(2)
        t = grid, start, goal
        li.append(t)
    u_pickle.dump(li, pickle_problems)


def run_a_with():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_with, 'w')
    file.write(f'i,nodes\n')
    for i, problem in enumerate(problems):
        grid, start, goal = problem
        astar = AStar(grid, start, goal)
        astar.run()
        file.write(f'{i},{astar.expanded_nodes()}\n')
    file.close()


def run_a_without():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_without, 'w')
    file.write(f'i,nodes\n')
    for i, problem in enumerate(problems):
        grid, start, goal = problem
        astar = AStar(grid, start, goal)
        astar.run()
        file.write(f'{i},{astar.expanded_nodes()}\n')
    file.close()


# create_problems()
# run_a_with()
# run_a_without()

problems = u_pickle.load(pickle_problems)
grid, start, goal = problems[47520]
print(start)
print(goal)
print(grid)
