from collections import Counter
from from model.point import Point
from from model.grid import Grid
from algo.astar_lookup import AStarLookup
from algo.kastar_backward import KAStarBackward
from logic.point_distance import LogicPointDistance as logic


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
        if type_forward_goal == 'NEAREST':
            self.goals = list(logic.points_nearest(start, goals).keys())
            self.goal_forward = self.goals[0]
            self.goals = set(self.goals) - {self.goal_forward}
        self.__run()

    def __run(self):
        """
        ========================================================================
         Description: Run the Algorithm.
        ========================================================================
        """
        astar = AStarLookup(self.grid, self.start, self.goal_forward)
        astar.run()
        lookup = astar.lookup_start()
        kastar = KAStarBackward(self.grid, self.start, self.goals, lookup,
                                self.type_next_goal)
        self.closed = kastar.closed
        self.closed.update(astar.closed)
