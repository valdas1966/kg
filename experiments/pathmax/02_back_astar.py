from algo.astar_lookup import AStarLookup
from f_utils import u_pickle
import config


li_back = list()
li_spp = u_pickle.load(config.dir_spp)
for spp in li_spp:
    astar = AStarLookup(grid=spp.grid,
                        start=spp.start,
                        goal=spp.goal,
                        lookup=spp.lookup)
    astar.run()



