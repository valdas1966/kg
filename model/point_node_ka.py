from model.point_node import Node


class NodeKA(Node):

    def __init__(self, point=None, x=None, y=None, active_goals=None):
        super().__init__(point, x, y)
        self.active_goals = None
        self.update_active_goals(active_goals)

    def update_active_goals(self, active_goals):
        self.active_goals = active_goals
        self.set_h()
        self.set_f()

    def set_h(self, true_distance=None):
        self.h = min(self.distance(goal) for goal in self.active_goals)
