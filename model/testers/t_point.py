from f_utils import u_tester
from model.point import Point


class TestPoint:

    def __init__(self):
        u_tester.print_start(__file__)
        TestPoint.__tester_in_rectangle()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_in_rectangle():
        point = Point(2, 2)
        p0 = point.in_rectangle(0, 0, 2, 2)
        p1 = not point.in_rectangle(0, 0, 9, 1)
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestPoint()
