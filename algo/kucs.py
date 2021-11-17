from model.opened import Opened
from model.point_node_g import Node


class KUCS:

    def __init__(self, grid, start, goals):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.active_goals = goals
        self.expanded_nodes = 0
        self.optimal_path
        self.closed = set()
        self.opened = Opened

    def run(self):
        self.opened.push(Node(self.start))
        while not self.opened.is_empty():
            best = self.opened.get_best()
            if best in self.active_goals:
                self.active_goals.remove(best)
                if not self.active_goals:
                    return



    def _generate_node(self):