from collections import defaultdict
from f_utils import u_file
from f_utils import u_pickle
from logic import u_grid_blocks
from algo.kastar_projection import KAStarProjection
from algo.kastar_backward import KAStarBackward
from algo.kastar_bi import KAStarBi
from f_utils import u_dict


path_dir = 'd:\\exp_big_maps_far\\'
path_maps = path_dir + 'Maps'
pickle_grids = path_dir + 'grids.pickle'
pickle_sg_potential = path_dir + 'sg_potential.pickle'
pickle_sg = path_dir + 'sg.pickle'
csv_sg_potential = path_dir + 'sg_potential.csv'
csv_sg = path_dir + 'sg.csv'
csv_forward = path_dir + 'forward.csv'
csv_backward = path_dir + 'backward.csv'
csv_bi = path_dir + 'bi.csv'


def create_grids():
    d_grids = defaultdict(list)
    for filepath in u_file.filepaths(path_maps):
        cat = filepath.split('\\')[-2]
        grid = u_grid_blocks.from_map(filepath)
        d_grids[cat].append(grid)
        print(filepath, grid.rows, grid.cols, len(grid.points()))
    u_pickle.dump(d_grids, pickle_grids)


def create_sg_potential():
    d_sg = dict()
    grids = u_pickle.load(pickle_grids)
    for cat, li_maps in grids.items():
        d_sg[cat] = dict()
        for map, grid in enumerate(li_maps):
            pairs = u_grid_blocks.random_pairs_by_distance(grid,
                                                           amount=10000000,
                                                           size=100)
            d_sg[cat][map] = pairs
            print(cat, map)
    u_pickle.dump(d_sg, pickle_sg_potential)


def print_sg_potential():
    d_sg = u_pickle.load(pickle_sg_potential)
    file = open(csv_sg_potential, 'w')
    file.write('cat,map,distance,pairs\n')
    for cat in d_sg:
        for map in sorted(d_sg[cat]):
            for distance in sorted(d_sg[cat][map]):
                pairs = d_sg[cat][map][distance]
                file.write(f'{cat},{map},{distance},{len(pairs)}\n')
    file.close()


def create_sg():
    d_grids = u_pickle.load(pickle_grids)
    d_potential = u_pickle.load(pickle_sg_potential)
    d_sg = dict()
    for cat in d_potential:
        d_sg[cat] = dict()
        for map in d_potential[cat]:
            grid = d_grids[cat][map]
            pairs = d_potential[cat][map][900]
            li_sg = list()
            for (start, goal_a) in pairs:
                goals = u_grid_blocks.random_points_radius(grid=grid,
                                                           point=goal_a,
                                                           radius=8, amount=9)
                if len(goals) == 9:
                    goals.append(goal_a)
                    li_sg.append((start, goals))
                    if len(li_sg) == 10:
                        break
            d_sg[cat][map] = li_sg
            print(cat, map)
    u_pickle.dump(d_sg, pickle_sg)


def print_sg():
    file = open(csv_sg, 'w')
    file.write('cat,map,length\n')
    d_sg_far = u_pickle.load(pickle_sg)
    for cat in d_sg_far:
        for map in sorted(d_sg_far[cat]):
            length = len(d_sg_far[cat][map])
            file.write(f'{cat},{map},{length}\n')
    file.close()


def create_forward():
    print('forward')
    file = open(csv_forward, 'w')
    file.write('cat,map,goals,i,nodes\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids)
    d_sg = u_pickle.load(pickle_sg)
    for cat in sorted(d_sg):
        for map in sorted(d_sg[cat]):
            grid = d_grids[cat][map]
            pairs = d_sg[cat][map]
            for i, (start, goals) in enumerate(pairs):
                d_goals = {goal: start.distance(goal) for goal in goals}
                d_goals = u_dict.sort_by_value(d_goals)
                goals = list(d_goals.keys())
                for k in range(2, 11):
                    kastar = KAStarProjection(grid, start, goals[:k])
                    kastar.run()
                    nodes = len(kastar.closed)
                    file = open(csv_forward, 'a')
                    file.write(f'{cat},{map},{k},{i},{nodes}\n')
                    file.close()
                    print(cat, map, i, k)


def create_backward():
    print('backward')
    file = open(csv_backward, 'w')
    file.write('cat,map,goals,i,nodes\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids)
    d_sg = u_pickle.load(pickle_sg)
    for cat in sorted(d_sg):
        for map in sorted(d_sg[cat]):
            grid = d_grids[cat][map]
            pairs = d_sg[cat][map]
            for i, (start, goals) in enumerate(pairs):
                d_goals = {goal: start.distance(goal) for goal in goals}
                d_goals = u_dict.sort_by_value(d_goals)
                goals = list(d_goals.keys())
                for k in range(2, 11):
                    kastar = KAStarBackward(grid, start, goals[:k],
                                            lookup=dict())
                    kastar.run()
                    nodes = sum(kastar.closed.values())
                    file = open(csv_backward, 'a')
                    file.write(f'{cat},{map},{k},{i},{nodes}\n')
                    file.close()
                    print(cat, map, i, k)


def create_bi():
    print('bi')
    file = open(csv_bi, 'w')
    file.write('cat,map,goals,i,nodes\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids)
    d_sg = u_pickle.load(pickle_sg)
    for cat in sorted(d_sg):
        for map in sorted(d_sg[cat]):
            grid = d_grids[cat][map]
            pairs = d_sg[cat][map]
            for i, (start, goals) in enumerate(pairs):
                d_goals = {goal: start.distance(goal) for goal in goals}
                d_goals = u_dict.sort_by_value(d_goals)
                goals = list(d_goals.keys())
                for k in range(2, 11):
                    kastar = KAStarBi(grid, start, goals[:k])
                    kastar.run()
                    nodes = sum(kastar.closed.values())
                    file = open(csv_bi, 'a')
                    file.write(f'{cat},{map},{k},{i},{nodes}\n')
                    file.close()
                    print(cat, map, i, k)


# create_grids
# create_sg_potential()
# print_sg_potential()
# create_sg()
# print_sg()
# create_forward()
# create_backward()
# create_bi()

grids = u_pickle.load(pickle_grids)
grid = grids['Cities'][1]
print(len(grid.points()))