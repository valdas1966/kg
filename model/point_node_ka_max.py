from model.point_node import NodeKA


class NodeKAMax(NodeKA):

    def set_h(self, true_distance=None):
        self.h = min(self.distance(goal) for goal in self.active_goals)
