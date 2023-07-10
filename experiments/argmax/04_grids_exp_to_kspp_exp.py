import config
from model.kspp import KSPP
from f_utils import u_pickle

"""
================================================================================
 Desc: [GridDomainMap] -> [KSPP_Domain_Map META]
       100 Grids (5 per Domain) -> 1500 KSPP (15 per Grid, 5 per k)
================================================================================
"""

path_grids_exp = config.path_grids_exp
path_kspp_exp = config.path_kspp_exp

pickle_grids_exp = f'{path_grids_exp}\\grids_exp.pickle'
pickle_kspp_exp = f'{path_kspp_exp}\\kspp_exp.pickle'


kspp_exp = list()
grids_exp = u_pickle.load(pickle_grids_exp)
for grid in grids_exp:
    for k in (2, 5, 10):
        li = KSPP.generate_random(grid=grid, n=5, k=k, radius=5)
        li = [kspp.to_meta() for kspp in li]
        kspp_exp.extend(li)
    print(len(kspp_exp))

u_pickle.dump(obj=kspp_exp, path=pickle_kspp_exp)
