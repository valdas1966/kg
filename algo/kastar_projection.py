from model.point import Point
from model.grid_blocks import GridBlocks
from model.opened import Opened
from logic.point_distance import LogicPointDistance
from algo.astar import AStar


class KAStarProjection:

    def __init__(self, grid, start, goals):
        """
        ========================================================================
         Description: Constructor - Init the arguments and sort the goals.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlocks
            2. start : Point
            3. goals : Set of Points
        ========================================================================
        """
        assert issubclass(type(grid), GridBlocks), f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(start)={type(start)}'
        assert type(goals) in [tuple, list, set], f'type(goals)={type(goals)}'
        assert len(goals) == len(set(goals))
        self.grid = grid
        self.start = start
        self.goals = LogicPointDistance.points_nearest(start, goals)
        self.opened = Opened()
        self.closed = set()
        self.__run()

    def __run(self):
        """
        ========================================================================
         Description: Run KA* Algo in Projective Mode (one Goal each run).
        ========================================================================
        """
        for goal in self.goals:
            if goal in self.closed:
                continue
            for node in self.opened.get_nodes():
                node.update(goal=goal)
            astar = AStar(self.grid, self.start, goal)
            astar.opened = self.opened
            astar.closed = self.closed
            astar.run()
            self.opened = astar.opened
            self.closed = astar.closed

