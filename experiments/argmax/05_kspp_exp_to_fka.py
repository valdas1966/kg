import config
from model.kspp import KSPP
from algo.kastar_projection import KAStarProjection
from f_utils import u_pickle

pickle_kspp_exp = f'{config.path_kspp_exp}\\kspp_exp.pickle'
pickle_fka = f'{config.path_fka}\\fka.pickle'

res = dict()
kspps = u_pickle.load(pickle_kspp_exp)
for i, kspp_meta in enumerate(kspps):
    domain, map, path, start, goals = kspp_meta
    kspp = KSPP.from_meta(domain, map, path, start, goals)
    ka = KAStarProjection(grid=kspp.grid,
                          start=kspp.start,
                          goals=kspp.goals)
    ka.run()
    res[kspp] = len(ka.closed)
    print(i, res[kspp])
u_pickle.dump(obj=res, path=pickle_fka)
