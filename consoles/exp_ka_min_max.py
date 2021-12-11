from algo.kastar_eager import KAStarEager
from model.point import Point
from model.grid_blocks import GridBlocks
from f_utils import u_pickle


repo = 'g:\\temp\\exp ka min max\\'
pickle_problems = repo + 'problems.pickle'
csv_results = repo + 'results_{0}.csv'


def create_problems():
    li = list()
    for _ in range(1000):
        grid = GridBlocks(rows=10, percent_blocks=20)
        start, goal_1, goal_2, goal_3, goal_4, goal_5 = grid.points_random(
            amount=6)
        goals = {goal_1, goal_2}
        li.append((grid, start, goals))
        goals.add(goal_3)
        li.append((grid, start, goals))
        goals.add(goal_4)
        goals.add(goal_5)
        li.append((grid, start, goals))
    u_pickle.dump(li, pickle_problems)


def run_ka(h):
    problems = u_pickle.load(pickle_problems)
    csv = csv_results.format(h)
    file = open(csv, 'w')
    file.write('i,nodes\n')
    for i, p in enumerate(problems):
        grid, start, goals = p
        kastar = KAStarEager(grid, start, goals)
        kastar.run()
        file.write(f'{i},{len(kastar.closed)}\n')
    file.close()



# create_problems()
run_ka('avg')
