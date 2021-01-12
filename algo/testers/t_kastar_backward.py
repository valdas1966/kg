from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.kastar_backward import KAStarBackward


class TestKAStarBackward:

    def __init__(self):
        u_tester.print_start(__file__)
        TestKAStarBackward.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        # Manual
        grid = GridBlocks(5)
        grid.set_block(1, 2)
        grid.set_block(1, 3)
        grid.set_block(2, 2)
        grid.set_block(3, 2)
        start = Point(2, 3)
        goals = [Point(0, 3), Point(0, 1), Point(0, 0)]
        kastar = KAStarBackward(grid, start, goals)
        closed_test = kastar.closed
        closed_true = {Point(0, 0): 1, Point(0, 1): 1, Point(0, 2): 2,
                       Point(0, 3): 1, Point(0, 4): 1, Point(1, 0): 1,
                       Point(1, 1): 2, Point(1, 4): 1, Point(2, 0): 1,
                       Point(2, 1): 2, Point(2, 3): 1, Point(2, 4): 1}
        p0 = closed_test == closed_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestKAStarBackward()
