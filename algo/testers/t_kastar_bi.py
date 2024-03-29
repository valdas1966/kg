from f_utils import u_tester
from model.point import Point
from model.grid_blocks import GridBlocks
from algo.kastar_bi import KAStarBi


class TestKAStarBi:

    def __init__(self):
        u_tester.print_start(__file__)
        TestKAStarBi.__tester_run()
        TestKAStarBi.__tester_run_found()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        grid = GridBlocks(5)
        grid.set_block(0, 3)
        grid.set_block(2, 3)
        grid.set_block(3, 3)
        grid.set_block(4, 3)
        start = Point(4, 4)
        goals = {Point(4, 2), Point(3, 1), Point(3, 0)}
        kastar = KAStarBi(grid, start, goals)
        kastar.run()
        closed_test = kastar.closed
        closed_true = {Point(1, 2): 1, Point(1, 3): 1, Point(1, 4): 1,
                       Point(2, 0): 1, Point(2, 1): 1, Point(2, 2): 1,
                       Point(2, 4): 1, Point(3, 0): 2, Point(3, 1): 1,
                       Point(3, 2): 1, Point(3, 4): 1, Point(4, 0): 2,
                       Point(4, 1): 2, Point(4, 2): 1, Point(4, 4): 1}
        p0 = closed_test == closed_true
        u_tester.run(p0)

    @staticmethod
    def __tester_run_found():
        grid = GridBlocks(5)
        start = Point(4, 4)
        goals = [Point(3, 3), Point(0, 0)]
        kastar = KAStarBi(grid, start, goals)
        kastar.run()
        p0 = kastar.is_found
        grid.set_block(0, 1)
        grid.set_block(1, 0)
        kastar = KAStarBi(grid, start, goals)
        kastar.run()
        p1 = not kastar.is_found
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestKAStarBi()
