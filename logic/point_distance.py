from proj.ai.model.point import Point
from f_utils import u_dict


class LogicPointDistance:

    @staticmethod
    def points_nearest(point_a, points_b):
        """
        ========================================================================
         Description: Return Dict of Points ordered by nearest distance
                        to the Point-A.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point_a : Point
            2. point_b : Set of Points
        ========================================================================
         Return: Dict {Point (Point B) -> int (Manhattan Distance to Point A).
        ========================================================================
        """
        assert type(point_a) == Point, f'type(point_a)={type(point_a)}'
        assert type(points_b) in [tuple, list, set], f'type=(points_b)=' \
                                                     f'{type(points_b)}'
        dict_points = dict()
        for point_b in set(points_b):
            dict_points[point_b] = point_a.distance(point_b)
        return u_dict.sort_by_value(dict_points)

    @staticmethod
    def distances_to(point_a, points_b):
        """
        ========================================================================
         Description: Return Average Distances between the Point A and Points B.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point_a : Point.
            2. points_b : Tuple | List | Set of Points.
        ========================================================================
         Return: int
        ========================================================================
        """
        assert type(point_a) == Point
        assert type(points_b) in [tuple, list, set]
        points_b = set(points_b)
        distances = 0
        for point_b in points_b:
            distances += point_a.distance(point_b)
        return int(distances / len(points_b))

    @staticmethod
    def distances(points):
        """
        ========================================================================
         Description: Return Average-Distance between the Points.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. points : [Tuple, List, Set] of Points
        ========================================================================
         Return: int
        ========================================================================
        """
        assert type(points) in [tuple, list, set]
        points = set(points)
        res = 0
        for point_a in points:
            for point_b in points - {point_a}:
                res += point_a.distance(point_b)
        return int(res / len(points))
