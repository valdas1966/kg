import config
import random
from f_utils import u_pickle


"""
================================================================================
 Desc: {domain: [GridDomainMap]} -> [GridDomainMap]
       All Maps -> 100 maps [20 per Domain]
================================================================================
"""

path_grids_all = config.path_grids_all
path_grids_exp = config.path_grids_exp

pickle_grids_all = f'{path_grids_all}\\grids_all.pickle'
pickle_grids_exp = f'{path_grids_exp}\\grids_exp.pickle'


grids_exp = list()
grids_all = u_pickle.load(path=pickle_grids_all)
for domain, grids in grids_all.items():
    grids_random = random.sample(grids, 20)
    grids_exp.extend(grids_random)
    print(domain, len(grids_exp))

u_pickle.dump(obj=grids_exp, path=pickle_grids_exp)
