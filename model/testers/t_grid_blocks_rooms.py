from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.grid_blocks_birooms import GridBlocksRooms


class TestGridBlocksRooms:

    def __init__(self):
        u_tester.print_start(__file__)
        TestGridBlocksRooms.__tester_walls_and_door()
        TestGridBlocksRooms.__tester_left_room()
        TestGridBlocksRooms.__tester_right_room()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_walls_and_door():
        grid_test = GridBlocksRooms(rows=5, corner=Point(2, 3),
                                    door=Point(2, 1))
        grid_true = GridBlocks(rows=5)
        grid_true.set_block(Point(2, 0))
        grid_true.set_block(Point(2, 2))
        grid_true.set_block(Point(2, 3))
        grid_true.set_block(Point(1, 3))
        grid_true.set_block(Point(0, 3))
        p0 = grid_test == grid_true
        u_tester.run(p0)

    @staticmethod
    def __tester_left_room():
        grid = GridBlocksRooms(rows=5, corner=Point(2, 3), door=Point(2, 1))
        left_test = grid.get_left_room()
        left_true = [Point(0, 0), Point(0, 1), Point(0, 2),
                     Point(1, 0), Point(1, 1), Point(1, 2)]
        p0 = left_test == left_true
        u_tester.run(p0)

    @staticmethod
    def __tester_right_room():
        grid = GridBlocksRooms(rows=5, corner=Point(2, 3), door=Point(2, 1))
        right_test = grid.get_right_room()
        right_true = [Point(0, 4),
                      Point(1, 4),
                      Point(2, 4),
                      Point(3, 0), Point(3, 1), Point(3, 2), Point(3, 3),
                      Point(3, 4), Point(4, 0), Point(4, 1), Point(4, 2),
                      Point(4, 3), Point(4, 4)]
        p0 = right_test == right_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestGridBlocksRooms()
