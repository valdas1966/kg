from f_utils import u_pickle
from f_utils.c_timer import Timer
from proj.ai.logic.grid_blocks_ghf import LogicGridBlocksGHF as logic


dir_results = 'D:\\Exp_RooMap\\'
pickle_grids = dir_results + 'grids.pickle'
format_g = dir_results + 'G\\{0}_{1}_{2}.pickle'


def create_g():
    timer = Timer()
    grids = u_pickle.load(pickle_grids)
    for i, grid in enumerate(grids):
        points = grid.points()
        for point in points:
            dict_g = logic.to_dict_g(grid, point)
            val_1 = str(i).zfill(2)
            val_2 = str(point.x).zfill(3)
            val_3 = str(point.y).zfill(3)
            pickle_g = format_g.format(val_1, val_2, val_3)
            u_pickle.dump(dict_g, pickle_g)
            elapsed = timer.elapsed()
            print(i, point, f'{elapsed:,}')

create_g()
