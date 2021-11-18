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
        self.opened = Opened()
        self.closed = set()
        self.best = Node(self.start)
        self.best.update(father_cand=None, goal=self.goal)
        self.opened.push(self.best)
        while not self.opened.is_empty():
            self.best = self.opened.pop()
            self.closed.add(self.best)
            if self.best == self.goal:
                self.is_found = True
                return
            self.__expand_best()

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

    def expanded_nodes(self):
        return len(self.closed) - 1

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
