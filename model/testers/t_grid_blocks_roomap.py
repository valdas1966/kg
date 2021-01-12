from f_utils import u_tester
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.model.grid_blocks_roomap import GridBlocksRooMap


class TestGridBlocksRooMap:

    def __init__(self):
        u_tester.print_start(__file__)
        TestGridBlocksRooMap.__tester_rooms()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_rooms():
        path = 'test_roomap.txt'
        grid = GridBlocksRooMap(path, size_room=5, goals_in_room_max=5)
        rooms_test = grid.rooms
        rooms_true = GridBlocks(4)
        rooms_true.set_block(0, 1)
        p0 = rooms_test == rooms_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestGridBlocksRooMap()
