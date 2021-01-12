from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.kastar_projection import KAStarProjection


class TestKAStarProjection:

    def __init__(self):
        u_tester.print_start(__file__)
        TestKAStarProjection.__tester_run_manual()
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


if __name__ == '__main__':
    TestKAStarProjection()
