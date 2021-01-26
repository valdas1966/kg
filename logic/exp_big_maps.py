from collections import defaultdict
from f_utils import u_file
from f_utils import u_pickle
from logic import u_grid_blocks


path_dir = 'g:\\exp_big_maps\\'
path_maps = path_dir + 'Maps'
pickle_grids = path_dir + 'grids.pickle'
pickle_sg = path_dir + 'sg.pickle'
csv_sg = path_dir + 'sg.csv'


def create_grids():
    d_grids = defaultdict(list)
    for filepath in u_file.filepaths(path_maps):
        cat = filepath.split('\\')[-2]
        grid = u_grid_blocks.from_map(filepath)
        d_grids[cat].append(grid)
        print(filepath, grid.rows, grid.cols, len(grid.points()))
    u_pickle.dump(d_grids, pickle_grids)


def create_sg():
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
    u_pickle.dump(d_sg, pickle_sg)


def print_sg():
    d_sg = u_pickle.load(pickle_sg)
    file = open(csv_sg, 'w')
    file.write('cat,map,distance,pairs\n')
    for cat in d_sg:
        for map in sorted(d_sg[cat]):
            for distance in sorted(d_sg[cat][map]):
                pairs = d_sg[cat][map][distance]
                file.write(f'{cat},{map},{distance},{len(pairs)}\n')
    file.close()


# create_grids
# create_sg()
print_sg()
