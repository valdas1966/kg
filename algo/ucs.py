from model.opened import Opened
from model.point_node_g import Node


class UCS:

    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.is_found = False
        self.best = None
        self.opened = Opened()
        self.closed = set()

    def run(self):
        self.opened = Opened
        self.closed = set()
        self.start.update(father_cand=None, goal=self.goal)
        self.opened.push(Node(self.start))
        while not self.opened.is_empty():
            self.best = self.opened.get_best()
            self.closed.add(self.best)
            if self.best == self.goal:
                self.is_found = True
                return
            self.__expand_best()

    def __expand_best(self):
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
