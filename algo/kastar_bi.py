from collections import Counter
from model.point import Point
from model.grid import Grid
from algo.astar_lookup import AStarLookup
from algo.kastar_backward import KAStarBackward
from logic import u_points


class KAStarBi:

    def __init__(self, grid, start, goals,
                 type_forward_goal='NEAREST', type_next_goal='NEAREST'):
        """
        ========================================================================
         Description: Create BiDirectional-KA*.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goals : Tuple | List | Set
            4. type_forward_goal : str (Method to choose the Forward Goal)
            5. type_next_goal : str (Method to choose the Next Goal)
        ========================================================================
        """
        assert issubclass(type(grid), Grid)
        assert type(start) == Point
        assert type(goals) in {tuple, list, set}
        assert type(type_forward_goal) == str
        assert type(type_next_goal) == str
        self.closed = Counter(list())
        self.grid = grid
        self.start = start
        self.goals = goals
        self.type_next_goal = type_next_goal
        self.goal_forward = None
        self.is_found = False
        if type_forward_goal == 'NEAREST':
            self.goals = list(u_points.nearest(start, goals).keys())
            self.goal_forward = self.goals[0]
            self.goals = set(self.goals) - {self.goal_forward}

    def run(self):
        """
        ========================================================================
         Description: Run the Algorithm.
        ========================================================================
        """
        self.is_found = True
        astar = AStarLookup(self.grid, self.start, self.goal_forward)
        astar.run()
        if not astar.is_found:
            self.is_found = False
            return
        lookup = astar.lookup_start()
        kastar = KAStarBackward(self.grid, self.start, self.goals, lookup,
                                self.type_next_goal)
        kastar.run()
        if not kastar.is_found:
            self.is_found = False
            return
        self.closed = kastar.closed
        self.closed.update(astar.closed)

    def expanded_nodes(self):
        return sum(self.closed.values())
