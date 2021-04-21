from f_utils import u_tester
from model.point import Point
from model.grid_blocks import GridBlocks
from logic import u_points


class TestPoints:

    def __init__(self):
        u_tester.print_start(__file__)
        TestPoints.__tester_nearest()
        TestPoints.__tester_distances()
        TestPoints.__tester_distances_to()
        TestPoints.__tester_distance_rows()
        TestPoints.__tester_distance_cols()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_nearest():
        point_a = Point(0, 0)
        points_b = {Point(2, 0), Point(0, 1), Point(1, 2)}
        nearest_test = u_points.nearest(point_a, points_b)
        nearest_true = {Point(0, 1): 1, Point(2, 0): 2, Point(1, 2):3}
        p0 = nearest_test == nearest_true
        u_tester.run(p0)

    @staticmethod
    def __tester_distances_to():
        point_a = Point(0, 0)
        points_b = [Point(0, 1), Point(1, 1), Point(2, 2), Point(2, 2)]
        distances_test = u_points.distances_to(point_a, points_b)
        distances_true = 2
        p0 = distances_test == distances_true
        u_tester.run(p0)

    @staticmethod
    def __tester_distances():
        points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(1, 2)]
        distances_test = u_points.distances(points)
        p0 = distances_test == 3.25
        u_tester.run(p0)

    @staticmethod
    def __tester_distance_rows():
        points_a = [Point(3, 3)]
        points_b = [Point(5, 5)]
        distance_test = u_points.distance_rows(points_a, points_b)
        p0 = distance_test == 2
        points_b = [Point(5, 5), Point(7, 7)]
        distance_test = u_points.distance_rows(points_a, points_b)
        p1 = distance_test == 3
        points_a = [Point(3, 3), Point(4, 4)]
        distance_test = u_points.distance_rows(points_a, points_b)
        p2 = distance_test == 2.5
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_distance_cols():
        points_a = [Point(3, 3)]
        points_b = [Point(5, 4)]
        distance_test = u_points.distance_cols(points_a, points_b)
        p0 = distance_test == 1
        points_b = [Point(5, 5), Point(7, 6)]
        distance_test = u_points.distance_cols(points_a, points_b)
        p1 = distance_test == 2.5
        points_a = [Point(3, 3), Point(4, 3)]
        distance_test = u_points.distance_cols(points_a, points_b)
        p2 = distance_test == 2.5
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestPoints()
