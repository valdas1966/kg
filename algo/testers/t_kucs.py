from f_utils import u_tester
from algo.kucs import KUCS
from model.point import Point
from model.grid_blocks import GridBlocks


class TestKucs:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        grid = GridBlocks(rows=5)
        start = Point(2, 2)
        goals = [Point(1, 2), Point(2, 4)]
        kucs = KUCS(grid, start, goals)
        kucs.run()
        p0 = kucs.expanded_nodes() == 9
        u_tester.run(p0)


if __name__ == '__main__':
    TestKucs()

