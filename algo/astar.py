from model.point import Point
from model.point_node import Node
from model.grid_blocks import GridBlocks
from model.opened import Opened


class AStar:
    """
    ============================================================================
     Description: AStar
    ============================================================================
    """

    def __init__(self, grid, start, goal):
        """
        ========================================================================
         Description: A* Algorithm.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : GridBlcoks
            2. start : Point
            3. goal : Point
        ========================================================================
        """
        assert issubclass(type(grid), GridBlocks), f'type(grid)={type(grid)}'
        assert type(start) == Point, f'type(start)={type(start)}'
        assert type(goal) == Point, f'type(goal)={type(goal)}'
        assert grid.is_valid_point(start)
        assert grid.is_valid_point(goal)
        self.start = start
        self.goal = goal
        self.name = f'{self.start.name}_{self.goal.name}'
        self.grid = grid
        self.is_found = False
        self.best = None
        self.closed = set()                     
        self.opened = Opened()

    def run(self):
        """
        ========================================================================
         Description: While the Search is not finished and the Opened is not
                        empty - Run the next move of the A* algorithm.
        ========================================================================
        """
        self.best = Node(self.start)
        self.best.update(father_cand=None, goal=self.goal)
        self.opened.push(self.best)
        while not self.opened.is_empty() and not self.is_found:
            self.next_move()

    def next_move(self):
        """
        ========================================================================
         Description: Run the next move of the Algorithm.
        ========================================================================
        """
        self.best = self.opened.pop()
        self.closed.add(self.best)
        self.__expand()
        if self.best == self.goal:
            self.is_found = True

    def optimal_path(self):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Return: List of Points.
        =======================================================================
        """
        if not self.is_found:
            return list()
        node = self.best
        path = [node]
        while node != self.start:
            node = node.father
            path.append(node)
        path.reverse()
        return path

    def f_value(self):
        """
        ========================================================================
         Description: Return the F-Value of the Goal.
        ========================================================================
         Return: int
        ========================================================================
        """
        if not self.is_found:
            return float('Infinity')
        return self.best.f

    def expanded_nodes(self):
        """
        ========================================================================
         Description: Return Amount of Expanded Nodes.
        ========================================================================
         Return: int
        ========================================================================
        """
        if self.is_found:
            # Goal-Node is not expanded
            return len(self.closed) - 1
        return len(self.closed)

    def __expand(self):
        """
        =======================================================================
         Description: Expand the Best.
        =======================================================================
        """
        points_neighbors = self.grid.neighbors(self.best)
        children = {point for point in points_neighbors} - self.closed
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            else:
                child = Node(child)
                self.opened.push(child)
            child.update(father_cand=self.best, goal=self.goal)
