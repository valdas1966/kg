from collections import defaultdict
from f_utils import u_file
from f_utils import u_pickle
from logic import u_grid_blocks


path_dir = 'g:\\exp_big_maps\\'
path_maps = path_dir + 'Maps'
pickle_grids = path_dir + 'grids.pickle'
pickle_sg_potential = path_dir + 'sg_potential.pickle'
pickle_sg = path_dir + 'sg.pickle'
csv_sg_potential = path_dir + 'sg_potential.csv'


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
    for cat in d_potential:
        for map in d_potential[cat]:
            for distance, pairs in d_potential[cat][map].items():
                if distance >= 1000:
                    continue
                li_sg = list()
                for (start, goal_a) in pairs:
                    print(len(li_sg))
                    grid = d_grids[cat][map]
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
                d_potential[cat][map][distance] = li_sg
                print(cat, map, distance)
    u_pickle.dump(d_potential, pickle_sg)


# create_grids
# create_sg()
# print_sg()
create_sg()
#