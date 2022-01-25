from model.point import Point
from model.point_node_ka import NodeKA
from model.grid_blocks import GridBlocks
from model.opened import Opened


class KAStarEager:

    def __init__(self, grid, start, goals):
        assert issubclass(type(grid), GridBlocks)
        assert type(start) == Point
        assert type(goals) in {tuple, list, set}
        self.grid = grid
        self.start = start
        self.goals = set(goals)
        self.active_goals = None
        self.opened = None
        self.closed = None
        self.is_found = None
        self.comp_h = 0

    def run(self):
        self.is_found = False
        self.active_goals = self.goals
        self.opened = Opened()
        self.closed = set()
        self.start = NodeKA(point=self.start, active_goals=self.active_goals)
        self.opened.push(self.start)
        while not self.opened.is_empty():
            best = self.opened.pop()
            self.closed.add(best)
            if best in self.active_goals:
                self.active_goals.remove(best)
                if not self.active_goals:
                    self.is_found = True
                    return
                for node in self.opened.get_nodes():
                    node.update_active_goals(self.active_goals)
                    self.comp_h += len(self.active_goals)
            self.__expand(best)

    def __expand(self, node):
        children = self.grid.neighbors(node)
        for child in sorted(children):
            if child in self.closed:
                continue
            elif self.opened.contains(child):
                child = self.opened.get(child)
            else:
                child = NodeKA(point=child, active_goals=self.active_goals)
                self.opened.push(child)
                self.comp_h += len(self.active_goals)
            child.update(father_cand=node)
