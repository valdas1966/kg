from model.grid_blocks import GridBlocks
from algo.astar import AStar
from algo.kastar_projection import KAStarProjection


def run():
    found = False
    while not found:
        grid = GridBlocks(rows=5, percent_blocks=20)
        points = grid.points_random(amount=3)
        start = points[0]
        goals = points[1:]
        ka = KAStarProjection(grid, start, goals)
        ka.run()
        forward = len(ka.closed)
        optimal_nodes = set()
        for goal in goals:
            astar = AStar(grid, start, goal)
            astar.run()
            optimal_nodes.update(astar.optimal_path())
        optimal = len(optimal_nodes)
        if optimal > forward:
            found = True
            print(optimal, forward)
            print(optimal_nodes)
            print(ka.closed)
            print(start)
            print(goals)
            print(grid)


run()

