from algo.astar import AStar


class KxAStar:

    def __init__(self, grid, start, goals):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.expanded_nodes = 0
        self.optimal_paths = dict()

    def run(self):
        self.expanded_nodes = 0
        for goal in self.goals:
            astar = AStar(self.grid, self.start, goal)
            astar.run()
            self.optimal_paths[goal] = astar.optimal_path()
            self.expanded_nodes += astar.expanded_nodes()
