from f_utils import u_tester
from logic import u_grid_blocks
from model.point import Point
from model.grid_blocks import GridBlocks


class TestGridBlocks:

    def __init__(self):
        u_tester.print_start(__file__)
        TestGridBlocks.__tester_sub_grid()
        TestGridBlocks.__tester_sub_grid_radius()
        TestGridBlocks.__tester_is_clean_line()
        TestGridBlocks.__tester_are_clean_line()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_sub_grid():
        grid = GridBlocks(5)
        grid.set_block(3, 3)
        sub_test = u_grid_blocks.sub_grid(grid, row_min=2, row_max=4,
                                          col_min=2, col_max=4)
        sub_true = GridBlocks(3)
        sub_true.set_block(1, 1)
        p0 = sub_test == sub_true
        u_tester.run(p0)

    @staticmethod
    def __tester_sub_grid_radius():
        grid = GridBlocks(5)
        grid.set_block(1, 2)
        point = Point(2, 2)
        sub_test = u_grid_blocks.sub_grid_radius(grid, point, radius=1)
        sub_true = GridBlocks(3)
        sub_true.set_block(0, 1)
        p0 = sub_test == sub_true
        point = Point(0, 0)
        sub_test = u_grid_blocks.sub_grid_radius(grid, point, radius=2)
        sub_true = GridBlocks(3)
        sub_true.set_block(1, 2)
        p1 = sub_test == sub_true
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_is_clean_line():
        grid = GridBlocks(5)
        point_a = Point(0, 1)
        point_b = Point(4, 1)
        p0 = u_grid_blocks.is_clean_line(grid, point_a, point_b)
        grid.set_block(2, 1)
        p1 = not u_grid_blocks.is_clean_line(grid, point_a, point_b)
        u_tester.run(p0, p1)

    @staticmethod
    def __tester_are_clean_line():
        grid = GridBlocks(3)
        grid.set_block(0, 1)
        point_a = Point(0, 0)
        point_b = Point(2, 0)
        point_c = Point(0, 2)
        points = {point_a, point_b}
        p0 = u_grid_blocks.are_clean_lines(grid, points)
        points.add(point_c)
        p1 = not u_grid_blocks.are_clean_lines(grid, points)
        u_tester.run(p0, p1)

    @staticmethod
    def tester_random_pairs_by_distance():
        grid = GridBlocks(7)
        grid.set_block(1, 3)
        grid.set_block(2, 3)
        grid.set_block(3, 1)
        grid.set_block(3, 2)
        grid.set_block(3, 3)
        grid.set_block(3, 4)
        grid.set_block(3, 5)
        grid.set_block(4, 3)
        grid.set_block(5, 3)
        d_pairs = u_grid_blocks.random_pairs_by_distance(grid, amount=10,
                                                         size=2)
        for distance in sorted(d_pairs.keys()):
            print(distance, d_pairs[distance])


if __name__ == '__main__':
    TestGridBlocks()

# TestGridBlocks.tester_random_pairs_by_distance()
#
