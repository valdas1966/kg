from f_utils import u_pickle

dir_results = 'D:\\Exp_RooMap\\3\\'
pickle_grids = dir_results + 'grids.pickle'

grids = u_pickle.load(pickle_grids)
for i, grid in enumerate(grids):
    print(i, grid.size_room)