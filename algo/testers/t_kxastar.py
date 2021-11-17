from f_utils import u_tester
from algo.kxastar import KxAStar
from model.grid_blocks import GridBlocks
from model.point import Point


class TestKxAStar:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_optimal_paths()
        self.__tester_expanded_nodes()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_optimal_paths():
        grid = GridBlocks(5)
        start = Point(3, 1)
        goal_1 = Point(1, 2)
        goal_2 = Point(2, 3)
        goals = [goal_1, goal_2]
        kxastar = KxAStar(grid, start, goals)
        kxastar.run()
        optimal_paths = kxastar.optimal_paths
        p0 = optimal_paths[goal_1] == [start, Point(2, 1), Point(1, 1), goal_1]
        p1 = optimal_paths[goal_2] == [start, Point(2, 1), Point(2, 2), goal_2]
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_expanded_nodes():
        grid = GridBlocks(5)
        start = Point(3, 1)
        goal_1 = Point(1, 2)
        goal_2 = Point(2, 3)
        goals = [goal_1, goal_2]
        kxastar = KxAStar(grid, start, goals)
        kxastar.run()
        p0 = kxastar.expanded_nodes == 6
        u_tester.run(p0)


if __name__ == '__main__':
    TestKxAStar()
