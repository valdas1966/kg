from f_utils import u_tester
from logic import u_grid
from model.point import Point
from model.grid import Grid


class TestGrid:

    def __init__(self):
        self.__tester_offsets()

    @staticmethod
    def __tester_offsets():
        grid = Grid(5)
        point = Point(1, 2)
        offsets_test = u_grid.offsets(grid, point)
        offsets_true = (1, 2, 3, 2)
        p0 = offsets_test == offsets_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestGrid()
