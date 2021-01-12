from f_utils import u_tester
from proj.ai.model.grid import Grid
from proj.ai.model.point import Point


class TestModelGrid:

    def __init__(self):
        u_tester.print_start(__file__)
        TestModelGrid.__tester_is_valid_point()
        TestModelGrid.__tester_neighbors()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_is_valid_point():
        grid = Grid(rows=3)
        point = Point(1, 1)
        p0 = grid.is_valid_point(point)
        point = Point(-1, 1)
        p1 = not grid.is_valid_point(point)
        point = Point(10, 1)
        p2 = not grid.is_valid_point(point)
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_neighbors():
        grid = Grid(rows=3)
        # Point in the middle of the Grid
        point = Point(1, 1)
        neighbors_test = grid.neighbors(point)
        neighbors_true = [Point(0, 1), Point(1, 0), Point(1, 2), Point(2, 1)]
        p0 = neighbors_test == neighbors_true
        # Point in the corner of the Grid
        point = Point(2, 2)
        neighbors_test = grid.neighbors(point)
        neighbors_true = [Point(1, 2), Point(2, 1)]
        p1 = neighbors_test == neighbors_true
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestModelGrid()
