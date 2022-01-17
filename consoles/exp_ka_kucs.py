from model.point import Point
from model.grid_blocks import GridBlocks
from algo.kucs import KUCS
from algo.kastar_eager import KAStarEager
from f_utils import u_pickle
import random


repo = 'g:\\temp\\thesis\\'
pickle_grids = repo + 'grids.pickle'
csv_results = repo + 'results.csv'

grids = list()
file = open(csv_results, 'w')
file.write('i,kucs,ka\n')
for i in range(1000):
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
        grids.append(grid)
        kucs = KUCS(grid, start, goals)
        kucs.run()
        file.write(f'{i},{kucs.expanded_nodes()},{len(ka.closed)}\n')
file.close()
u_pickle.dump(grids, pickle_grids)



