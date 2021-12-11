from model.point import Point
from model.grid_blocks import GridBlocks
from algo.kastar_projection import KAStarProjection
from algo.kastar_eager import KAStarEager
from f_utils import u_pickle

csv = 'g:\\temp\\exp_ka_eager_vs_projection.csv'
pickle = 'g:\\temp\\exp_ka_eager_vs_projeciton.pickle'


def run_exp():
    li = list()
    file = open(csv, 'w')
    file.write('i,proj,eager,delta\n')
    for i in range(100000):
        grid = GridBlocks(rows=5, percent_blocks=20)
        start, goal_1, goal_2 = grid.points_random(amount=3)
        goals = {goal_1, goal_2}
        ka_proj = KAStarProjection(grid, start, goals)
        ka_proj.run()
        ka_eager = KAStarEager(grid, start, goals)
        ka_eager.run()
        closed_proj = sorted(Point(n.x, n.y) for n in ka_proj.closed)
        closed_eager = sorted(Point(n.x, n.y) for n in ka_eager.closed)
        li.append((start, goals, grid, closed_proj, closed_eager))
        proj = len(ka_proj.closed)
        eager = len(ka_eager.closed)
        delta = proj - eager
        file.write(f'{i},{proj},{eager},{delta}\n')
    file.close()
    u_pickle.dump(li, pickle)


def print_record(index):
    record = u_pickle.load(pickle)[index]
    for item in record:
        if type(item) == set:
            print(sorted(Point(n.x, n.y) for n in item))
        else:
            print(item)


# run_exp()
print_record(74620)

