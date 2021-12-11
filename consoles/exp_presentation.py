from model.grid_blocks import GridBlocks
from algo.kucs import KUCS
from algo.kxastar import KxAStar
from algo.kastar_eager import KAStarEager
from algo.kastar_backward import KAStarBackward
from algo.kastar_bi import KAStarBi
from f_utils import u_pickle
from f_utils import u_int
from random import randint


repo = 'g:\\temp\\exp presentation\\'
pickle_problems = repo + 'problems.pickle'
csv_resutls = repo + 'results.csv'

def create_problems():
    li = list()
    for _ in range(500000):
        percent_blocks = randint(0, 20)
        grid = GridBlocks(rows=5, percent_blocks=percent_blocks)
        start, goal_1, goal_2 = grid.points_random(amount=3)
        li.append((grid, start, {goal_1, goal_2}))
    u_pickle.dump(li, pickle_problems)


def run_algo():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_resutls, 'w')
    file.write('i,kucs,kxa,ka,back,bi\n')
    for i, (grid, start, goals) in enumerate(problems):
        if not i%1000:
            print(u_int.to_commas(i))
        kucs = KUCS(grid, start, goals)
        kucs.run()
        nodes_kucs = kucs.expanded_nodes()
        kxastar = KxAStar(grid, start, goals)
        kxastar.run()
        nodes_kxastar = kxastar.expanded_nodes
        kastar = KAStarEager(grid, start, goals)
        kastar.run()
        nodes_kastar = len(kastar.closed)
        back = KAStarBackward(grid, start, goals, lookup=dict())
        back.run()
        nodes_back = len(back.closed)
        bi = KAStarBi(grid, start, goals)
        bi.run()
        nodes_bi = len(bi.closed)
        file.write(f'{i},{nodes_kucs},{nodes_kxastar},{nodes_kastar},'
                   f'{nodes_back},{nodes_bi}\n')
    file.close()


def print_problem(i):
    problems = u_pickle.load(pickle_problems)
    grid, start, goals = problems[i]
    print(start)
    print(goals)
    print(grid)

#create_problems()
# run_algo()
print_problem(155987)

"""
problems = u_pickle.load(pickle_problems)
grid, start, goals = problems[194136]
kastar = KAStarEager(grid, start, goals)
kastar.run()
"""



