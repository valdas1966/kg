from model.grid_blocks import GridBlocks
from algo.kastar_projection import KAStarProjection
from algo.kastar_bi import KAStarBi
from algo.kastar_backward import KAStarBackward
from f_utils import u_pickle
from f_db.c_sqlite import SQLite
import random
import pandas as pd


#repo = 'd:\\temp\\write\\exp ka directions\\'
repo = 'g:\\temp\\thesis\\exp ka directions 5 rows\\'
pickle_problems = repo + 'problems.pickle'
csv_results = repo + 'results.csv'


def create_problems():
    problems = list()
    i = 0
    while i < 500000:
        grid = GridBlocks(rows=5, percent_blocks=20)
        points = grid.points_random(amount=3)
        start = points[0]
        goals = points[1:]
        ka = KAStarProjection(grid, start, goals)
        ka.run()
        if not ka.is_found:
            continue
        problems.append((grid, start, goals))
        if not i % 1000:
            print(i)
        i += 1
    u_pickle.dump(problems, pickle_problems)


def run():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_results, 'w')
    file.write('i,forward,bi,backward,oracle,optimal,winner\n')
    for i, p in enumerate(problems):
        grid, start, goals = p
        ka_forward = KAStarProjection(grid, start, goals)
        ka_forward.run()
        forward = len(ka_forward.closed)
        optimal_nodes = set()
        for li in ka_forward.optimal_paths.values():
            optimal_nodes.update(set(li))
        optimal = len(optimal_nodes)
        ka_bi = KAStarBi(grid, start, goals)
        ka_bi.run()
        bi = ka_bi.expanded_nodes()
        ka_backward = KAStarBackward(grid, start, goals)
        ka_backward.run()
        backward = ka_backward.expanded_nodes()
        oracle = min(forward, bi, backward)
        winner = 'Forward'
        if oracle == backward:
            winner = 'Backward'
        elif oracle == bi:
            winner = 'Bi'
        file.write(f'{i},{forward},{bi},{backward},{oracle},'
                   f'{optimal},{winner}\n')
        if not i % 1000:
            print(i)
    file.close()


def show_problem(i):
    problem = u_pickle.load(pickle_problems)[i]
    grid, start, goals = problem
    print(start)
    print(goals)
    print(grid)

#create_problems()
#run()
show_problem(191703)