from model.point import Point
from model.grid_blocks import GridBlocks
from algo.kucs import KUCS
from algo.kxastar import KxAStar
from f_utils import u_pickle


path_repo = 'd:\\temp\\write\\'
pickle_problems = path_repo + 'problems.pickle'
csv_kucs = path_repo + 'kucs.csv'
csv_kxastar = path_repo + 'kxastar.csv'


def create_problems():
    problems = list()
    for _ in range(1000):
        grid = GridBlocks(rows=5, percent_blocks=20)
        start, goal_1, goal_2 = grid.points_random(amount=3)
        problem = grid, start, [goal_1, goal_2]
        problems.append(problem)
    u_pickle.dump(problems, pickle_problems)


def run_kucs():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_kucs, 'w')
    file.write('i,kucs\n')
    for i, problem in enumerate(problems):
        grid, start, goals = problem
        kucs = KUCS(grid, start, goals)
        kucs.run()
        if kucs.is_found:
            file.write(f'{i},{kucs.expanded_nodes()}\n')
    file.close()


def run_kxastar():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_kxastar, 'w')
    file.write('i,kxastar\n')
    for i, problem in enumerate(problems):
        grid, start, goals = problem
        kxastar = KxAStar(grid, start, goals)
        kxastar.run()
        if kxastar.is_found:
            file.write(f'{i},{kxastar.expanded_nodes}\n')
    file.close()


# create_problems()
# run_kucs()
# run_kxastar()

problems = u_pickle.load(pickle_problems)
problem = problems[74]
grid, start, goals = problem
print(start)
print(goals)
print(grid)
