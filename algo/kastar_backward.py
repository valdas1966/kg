from collections import Counter
from from model.point import Point
from from model.grid import Grid
from algo.astar_lookup import AStarLookup
from logic.point_distance import LogicPointDistance as logic


class KAStarBackward:

    def __init__(self, grid, start, goals, lookup=dict(),
                 type_next_goal='NEAREST'):
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
            self.goals = list(logic.points_nearest(start, goals).keys())
        self.__run()

    def __run(self):
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


"""
from f_utils import u_pickle

dir_results = 'D:\\Exp_RooMap\\'
pickle_grids = dir_results + 'grids.pickle'
pickle_start_goals = dir_results + 'start_goals.pickle'

grids = u_pickle.load(pickle_grids)
grid = grids[0]

sg = u_pickle.load(pickle_start_goals)
start, goals = sg[0][4]

kastar = KAStarBackward(grid, start, goals)
print(kastar.start, kastar.goals)
print(sum(kastar.closed.values()))
"""