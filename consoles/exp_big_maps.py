from collections import defaultdict
from f_utils import u_file
from f_utils import u_pickle
from logic import u_grid_blocks
from algo.kastar_projection import KAStarProjection
from algo.kastar_backward import KAStarBackward
from algo.kastar_bi import KAStarBi


path_dir = 'g:\\exp_big_maps\\'
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
            d_sg[cat][map] = dict()
            grid = d_grids[cat][map]
            for distance, pairs in d_potential[cat][map].items():
                if distance >= 1000:
                    continue
                li_sg = list()
                for (start, goal_a) in pairs:
                    goals = u_grid_blocks.random_satellites(grid=grid,
                                                            point=goal_a,
                                                            radius=4,
                                                            amount=2,
                                                            epochs=1000)
                    if len(goals) == 2:
                        goal_b, goal_c = goals
                        li_sg.append((start, (goal_a, goal_b, goal_c)))
                        if len(li_sg) == 10:
                            break
                d_sg[cat][map][distance] = li_sg
                print(cat, map, distance)
    u_pickle.dump(d_sg, pickle_sg)


def print_sg():
    file = open(csv_sg, 'w')
    file.write('cat,map,distance,length\n')
    d_sg = u_pickle.load(pickle_sg)
    for cat in d_sg:
        for map in sorted(d_sg[cat]):
            for distance in sorted(d_sg[cat][map]):
                length = len(d_sg[cat][map][distance])
                file.write(f'{cat},{map},{distance},{length}\n')
    file.close()


def create_forward():
    print('forward')
    file = open(csv_forward, 'w')
    file.write('cat,map,distance,i,forward_2,forward_3\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids)
    d_sg = u_pickle.load(pickle_sg)
    for cat in sorted(d_sg):
        for map in sorted(d_sg[cat]):
            grid = d_grids[cat][map]
            for distance in sorted(d_sg[cat][map]):
                for i, pair in enumerate(sorted(d_sg[cat][map][distance])):
                    start, goals = pair
                    kastar_2 = KAStarProjection(grid, start, goals[:2])
                    kastar_2.run()
                    nodes_2 = len(kastar_2.closed)
                    kastar_3 = KAStarProjection(grid, start, goals[:3])
                    kastar_3.run()
                    nodes_3 = len(kastar_3.closed)
                    file = open(csv_forward, 'a')
                    file.write(f'{cat},{map},{distance},'
                               f'{i},{nodes_2},{nodes_3}\n')
                    file.close()
                print(cat, map, distance)
    file.close()


def create_backward():
    print('backward')
    file = open(csv_backward, 'w')
    file.write('cat,map,distance,i,backward_2,backward_3\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids)
    d_sg = u_pickle.load(pickle_sg)
    for cat in sorted(d_sg):
        for map in sorted(d_sg[cat]):
            grid = d_grids[cat][map]
            for distance in sorted(d_sg[cat][map]):
                for i, pair in enumerate(sorted(d_sg[cat][map][distance])):
                    start, goals = pair
                    kastar_2 = KAStarBackward(grid, start, goals[:2],
                                              lookup=dict())
                    kastar_2.run()
                    nodes_2 = sum(kastar_2.closed.values())
                    kastar_3 = KAStarBackward(grid, start, goals[:3],
                                              lookup=dict())
                    kastar_3.run()
                    nodes_3 = sum(kastar_3.closed.values())
                    file = open(csv_backward, 'a')
                    file.write(f'{cat},{map},{distance},'
                               f'{i},{nodes_2},{nodes_3}\n')
                    file.close()
                print(cat, map, distance)
    file.close()


def create_bi():
    print('bi')
    file = open(csv_bi, 'w')
    file.write('cat,map,distance,i,bi_2,bi_3\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids)
    d_sg = u_pickle.load(pickle_sg)
    for cat in sorted(d_sg):
        for map in sorted(d_sg[cat]):
            grid = d_grids[cat][map]
            for distance in sorted(d_sg[cat][map]):
                for i, pair in enumerate(sorted(d_sg[cat][map][distance])):
                    start, goals = pair
                    kastar_2 = KAStarBi(grid, start, goals[:2])
                    kastar_2.run()
                    nodes_2 = sum(kastar_2.closed.values())
                    kastar_3 = KAStarBi(grid, start, goals[:3])
                    kastar_3.run()
                    nodes_3 = sum(kastar_3.closed.values())
                    file = open(csv_bi, 'a')
                    file.write(f'{cat},{map},{distance},'
                               f'{i},{nodes_2},{nodes_3}\n')
                    file.close()
                print(cat, map, distance)
    file.close()


# create_grids
# create_sg()
# print_sg()
# create_sg()
# print_sg()
# create_forward()
# create_backward()
create_bi()
