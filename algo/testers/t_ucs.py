from f_utils import u_tester
from algo.ucs import UCS
from algo.astar import AStar
from model.point import Point
from model.grid_blocks import GridBlocks


class TestUCS:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_optimal_path()
        self.__tester_expanded_nodes()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_optimal_path():
        p0 = True
        for _ in range(100):
            grid = GridBlocks(rows=10, cols=10, percent_blocks=25)
            start, goal = grid.points_random(amount=2)
            ucs = UCS(grid, start, goal)
            ucs.run()
            astar = AStar(grid, start, goal)
            astar.run()
            if not len(ucs.optimal_path()) == len(astar.optimal_path()):
                p0 = False
                break
        u_tester.run(p0)

    @staticmethod
    def __tester_expanded_nodes():
        grid = GridBlocks(rows=5)
        grid.set_block(1, 2)
        grid.set_block(2, 2)
        grid.set_block(3, 2)
        grid.set_block(4, 2)
        start = Point(3, 1)
        goal = Point(3, 3)
        ucs = UCS(grid, start, goal)
        ucs.run()
        p0 = ucs.expanded_nodes() == 17
        u_tester.run(p0)


if __name__ == '__main__':
    TestUCS()

