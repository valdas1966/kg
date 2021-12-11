from algo.kastar_eager import KAStarEager
from algo.kastar_eager_closed import KAStarEagerClosed
from model.grid_blocks import GridBlocks
from model.point import Point
from f_utils import u_pickle


csv = 'g:\\temp\\exp_ka_eager_closed.csv'
pickle = 'g:\\temp\\exp_ka_eager.pickle'


def run_exp():
    li = list()
    file = open(csv, 'w')
    file.write('i,eager,closed,delta\n')
    for i in range(10000):
        grid = GridBlocks(rows=10, percent_blocks=20)
        start, goal_1, goal_2 = grid.points_random(amount=3)
        goals = {goal_1, goal_2}
        ka_eager = KAStarEager(grid, start, goals)
        ka_eager.run()
        ka_closed = KAStarEagerClosed(grid, start, goals)
        ka_closed.run()
        file.write(f'{i},{len(ka_eager.closed)},{len(ka_closed.closed_all)},'
                   f'{len(ka_eager.closed)-len(ka_closed.closed_all)}\n')
        closed_eager = sorted(Point(n.x, n.y) for n in ka_eager.closed)
        closed_closed = sorted(Point(n.x, n.y) for n in ka_closed.closed_all)
        li.append((start, grid, goals, closed_eager, closed_closed))
    file.close()
    u_pickle.dump(li, pickle)


def print_record(index):
    record = u_pickle.load(pickle)[index]
    for item in record:
        print(item)


run_exp()
# print_record(374)
