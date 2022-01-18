from model.point import Point
from model.grid_blocks import GridBlocks
from algo.kxastar import KxAStar
from algo.kastar_eager import KAStarEager
from f_utils import u_pickle
import random


repo = 'd:\\temp\\write\\exp ka kxa\\'
pickle_problems = repo + 'problems.pickle'
csv_results = repo + 'results.csv'

def run():
    problems = list()
    file = open(csv_results, 'w')
    file.write('i,blocks,goals,kxa,ka\n')
    for i in range(100000):
        is_found = False
        while not is_found:
            percent_blocks = random.randint(1, 80)
            grid = GridBlocks(rows=5, percent_blocks=percent_blocks)
            cnt_goals = random.randint(2, 4)
            points = grid.points_random(amount=cnt_goals+1)
            start = points[0]
            goals = points[1:]
            ka = KAStarEager(grid, start, goals)
            ka.run()
            if not ka.is_found:
                continue
            is_found = ka.is_found
            problems.append((grid, start, goals))
            kxa = KxAStar(grid, start, goals)
            kxa.run()
            file.write(f'{i}, {percent_blocks}, {cnt_goals},'
                       f'{kxa.expanded_nodes},{len(ka.closed)}\n')
            print(i)
    file.close()
    u_pickle.dump(problems, pickle_problems)


def show_problem(i):
    problems = u_pickle.load(pickle_problems)
    grid, start, goals = problems[i]
    print(start)
    print(goals)
    print(grid)


#run()
show_problem(81357)
