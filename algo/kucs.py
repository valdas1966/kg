from model.opened import Opened
from model.point_node_g import Node


class KUCS:

    def __init__(self, grid, start, goals):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.active_goals = set(goals)
        self.is_found = False
        self.best = None
        self.opened = Opened()
        self.closed = set()

    def run(self):
        self.opened = Opened()
        self.closed = set()
        self.best = Node(self.start)
        self.best.update(father_cand=None, goal=list(self.goals)[0])
        self.opened.push(self.best)
        while not self.opened.is_empty():
            self.best = self.opened.pop()
            self.closed.add(self.best)
            if self.best in self.active_goals:
                self.active_goals.remove(self.best)
                if not self.active_goals:
                    self.is_found = True
                    return
            self.__expand_best()

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
            child.update(father_cand=self.best, goal=list(self.goals)[0])
