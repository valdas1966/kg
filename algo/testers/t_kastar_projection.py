from f_utils import u_tester
from model.point import Point
from model.grid_blocks import GridBlocks
from algo.kastar_projection import KAStarProjection


class TestKAStarProjection:

    def __init__(self):
        u_tester.print_start(__file__)
        TestKAStarProjection.__tester_run_manual()
        TestKAStarProjection.__tester_run_found()
        TestKAStarProjection.__tester_optimal_paths()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run_manual():
        grid = GridBlocks(rows=4)
        # Perfect Heuristic (without blocks)
        start = Point(0, 0)
        goals = {Point(3, 3), Point(3, 0)}
        kastar = KAStarProjection(grid, start, goals)
        kastar.run()
        closed_test = kastar.closed
        closed_true = {Point(0, 0),
                       Point(1, 0),
                       Point(2, 0),
                       Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3)}
        p0 = closed_test == closed_true
        # Not-Perfect Heuristic (with blocks)
        grid.set_block(Point(2, 2))
        grid.set_block(Point(3, 2))
        kastar = KAStarProjection(grid, start, goals)
        kastar.run()
        closed_test = kastar.closed
        closed_true = {Point(0, 0),
                       Point(1, 0), Point(1, 1), Point(1, 2), Point(1, 3),
                       Point(2, 0), Point(2, 1), Point(2, 3),
                       Point(3, 0), Point(3, 1), Point(3, 3)}
        p1 = closed_test == closed_true
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_run_found():
        grid = GridBlocks(5)
        start = Point(4, 4)
        goals = [Point(3, 3), Point(0, 0)]
        kastar = KAStarProjection(grid, start, goals)
        kastar.run()
        p0 = kastar.is_found
        grid.set_block(0, 1)
        grid.set_block(1, 0)
        kastar = KAStarProjection(grid, start, goals)
        kastar.run()
        p1 = not kastar.is_found
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_optimal_paths():
        grid = GridBlocks(rows=5)
        grid.set_block(2, 3)
        grid.set_block(4, 3)
        start = Point(3, 2)
        goals = {Point(1, 4), Point(4, 4)}
        kastar = KAStarProjection(grid, start, goals)
        kastar.run()
        path_1 = [Point(3, 2), Point(3, 3), Point(3, 4), Point(2, 4),
                  Point(1, 4)]
        path_2 = [Point(3, 2), Point(3, 3), Point(3, 4), Point(4, 4)]
        optimal_paths_true = {Point(1, 4): path_1, Point(4, 4): path_2}
        p0 = kastar.optimal_paths == optimal_paths_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestKAStarProjection()
