from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.astar_lookup_early import AStarLookupEarly


class TestAStarLookupEarly:

    def __init__(self):
        u_tester.print_start(__file__)
        TestAStarLookupEarly.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        grid = GridBlocks(rows=3)
        start = Point(0, 0)
        goal = Point(2, 2)
        lookup = {Point(1, 0): 100}
        astar = AStarLookupEarly(grid, start, goal, lookup)
        astar.run()
        p0 = astar.best == Point(1, 0)
        p1 = astar.closed == {Point(0, 0)}
        p2 = astar.f_value() == 101
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestAStarLookupEarly()
