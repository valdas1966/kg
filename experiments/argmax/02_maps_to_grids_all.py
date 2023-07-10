from collections import defaultdict
from model.grid_domain_map import GridDomainMap
from f_utils import u_pickle
from f_utils import u_file
from f_utils import u_dir
import config


path_maps = config.path_maps
path_grids_all = config.path_grids_all

"""
for path_domain in u_dir.names_dirs(path=path_maps):
    domain = path_domain.split('\\')[-1]
    for path_map in u_file.filepaths(path_dir=path_domain):
        grid = u_grid_blocks.from_map(path=path_map)
        filename = u_file.get_filename(path=path_map, with_domain=False)
        path_pickle = f'{path_grids}\\{domain}_{filename}.pickle'.lower()
        u_pickle.dump(obj=grid, path=path_pickle)
        print(path_pickle)
"""

grids_all = defaultdict(list)
for path_domain in u_dir.names_dirs(path=path_maps):
    domain = path_domain.split('\\')[-1]
    for path_map in u_file.filepaths(path_dir=path_domain):
        map = u_file.get_filename(path=path_map, with_domain=False)
        grid = GridDomainMap(domain=domain, map=map, path=path_map)
        grids_all[domain].append(grid)
        print(domain, map)
path_pickle = f'{path_grids_all}\\grids_all.pickle'
u_pickle.dump(obj=grids_all, path=path_pickle)
