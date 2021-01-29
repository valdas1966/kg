from collections import Counter
from model.point import Point
from model.grid import Grid
from algo.astar_lookup import AStarLookup
from logic import u_points


class KAStarBackward:

    def __init__(self, grid, start, goals, lookup, type_next_goal='NEAREST'):
        """
        ========================================================================
         Description: Create KA*-Backward Algorithm (Use Optimal-Path Nodes
                        from previous searches for Lookup).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goals : Tuple | List | Set
            4. lookup : Dict of {Point: int (True-Distance to Start}.
            5. type_next_goal : str (Method to choose the next Goal)
        ========================================================================
        """
        assert issubclass(type(grid), Grid)
        assert type(start) == Point
        assert type(goals) in {tuple, list, set}
        assert type(lookup) == dict
        self.closed = Counter(list())
        self.grid = grid
        self.start = start
        self.goals = goals
        self.lookup = lookup
        if type_next_goal == 'NEAREST':
            self.goals = list(u_points.nearest(start, goals).keys())

    def run(self):
        """
        ========================================================================
         Description: Run the Algorithm.
        ========================================================================
        """
        li_closed = list()
        for goal in self.goals:
            astar = AStarLookup(grid=self.grid, start=goal, goal=self.start,
                                lookup=self.lookup)
            astar.run()
            li_closed = li_closed + list(astar.closed)
            self.lookup.update(astar.lookup_goal())
        self.closed = Counter(li_closed)
