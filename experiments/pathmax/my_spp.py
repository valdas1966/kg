from itertools import combinations
from model.grid_blocks import GridBlocks
from algo.astar_lookup import AStarLookup
from logic import u_grid_blocks
from experiments.pathmax import u_features


class MySPP:

    def __init__(self,
                 rows: int,               # Rows of the Grid
                 cols: int,               # Cols of the Grid
                 percent_blocks: int,     # Percent of Blocks in the Grid
                 radius_bc: int) -> None:  # Distance from B to C
        self.rows = rows
        self.cols = cols
        self.percent_blocks = percent_blocks
        self.radius_bc = radius_bc
        is_valid = False
        while not is_valid:
            self.grid = GridBlocks(rows=rows,
                                   cols=cols,
                                   percent_blocks=percent_blocks)
            self.nodes = self.__get_nodes()
            if not self.nodes:
                continue
            self.astars = self.__get_astars(self.nodes)
            if not all(astar.is_found for astar in self.astars.values()):
                continue
            self.lookup = self.astars['c_a'].lookup_goal()
            if self.nodes['b'] in self.lookup:
                continue
            astar_lookup = AStarLookup(grid=self.grid,
                                       start=self.nodes['b'],
                                       goal=self.nodes['a'],
                                       lookup=self.lookup)
            astar_lookup.run()
            astar_lookup.name = 'b_a_lookup_c_a'
            self.astars[astar_lookup.name] = astar_lookup
            is_valid = True

    def __get_nodes(self) -> dict:
        nodes = dict()
        nodes['a'], nodes['b'] = self.grid.points_random(amount=2)
        nodes['a'].name, nodes['b'].name = 'a', 'b'
        nodes['c'] = u_grid_blocks.random_points_radius(grid=self.grid,
                                                        point=nodes['b'],
                                                        radius=self.radius_bc,
                                                        amount=1)[0]
        if not nodes['c']:
            return None
        nodes['c'].name = 'c'
        return nodes

    def __get_astars(self, nodes: dict) -> dict:
        res = dict()
        vals = nodes.values()
        for a, b in combinations(vals, 2):
            astar_ab = AStarLookup(grid=self.grid, start=a, goal=b)
            astar_ab.run()
            res[astar_ab.name] = astar_ab
            astar_ba = AStarLookup(grid=self.grid, start=b, goal=a)
            astar_ba.run()
            res[astar_ba.name] = astar_ba
        return res

    def get_meta(self) -> dict:
        meta = dict()
        meta['rows'] = self.rows
        meta['cols'] = self.cols
        meta['percent_blocks'] = self.percent_blocks
        meta['radius_bc'] = self.radius_bc
        meta['nodes_grid'] = len(self.grid.points())
        meta.update(u_features.distances(nodes=self.nodes))
        meta.update(u_features.from_center(grid=self.grid, nodes=self.nodes))
        meta.update(u_features.closed(astars=self.astars))
        meta.update(u_features.optimal(astars=self.astars))
        meta.update(u_features.inter(astars=self.astars))
        return meta
