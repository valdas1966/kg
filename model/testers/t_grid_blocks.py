from f_utils import u_tester
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.point import Point


class TestModelGridBlocks:

    def __init__(self):
        u_tester.print_start(__file__)
        TestModelGridBlocks.__tester_is_valid_point()
        TestModelGridBlocks.__tester_neighbors()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_is_valid_point():
        grid = GridBlocks(rows=3)
        grid.set_block(x=1, y=1)
        point = Point(0, 0)
        p0 = grid.is_valid_point(point)
        point = Point(1, 1)
        p1 = not grid.is_valid_point(point)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_neighbors():
        grid = GridBlocks(rows=3)
        grid.set_block(x=1, y=1)
        point = Point(0, 1)
        neighbors_test = grid.neighbors(point)
        neighbors_true = [Point(0, 0), Point(0, 2)]
        p0 = neighbors_test == neighbors_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestModelGridBlocks()
