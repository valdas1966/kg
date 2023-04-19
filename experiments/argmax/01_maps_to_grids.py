from logic import u_grid_blocks
from f_utils import u_pickle
from f_utils import u_file
from f_utils import u_dir


path_argmax = 'd:\\temp\\kg\\argmax'
path_maps = f'{path_argmax}\\01 maps'
path_grids = f'{path_argmax}\\02 grids'

for path_domain in u_dir.names_dirs(path=path_maps):
    print(path_domain)
    for path_map in u_file.filepaths(path_dir=path_domain):
        grid = u_grid_blocks.from_map(path=path_map)
        u_pickle.dump(obj=grid, path)
        print(path_map)
