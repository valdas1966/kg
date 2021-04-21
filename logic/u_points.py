from model.point import Point
from f_utils import u_dict
import statistics


def nearest(point_a, points_b):
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
    summer = 0
    for point_b in points_b:
        summer += point_a.distance(point_b)
    return int(summer / len(points_b))


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
    assert type(points) in {tuple, list, set}
    points = sorted(set(points))
    res = 0
    for p_a in points:
        for p_b in points:
            if p_a >= p_b:
                continue
            res += p_a.distance(p_b)
    return res / len(points)


def distance_rows(points_a, points_b):
    """
    ============================================================================
     Description: Return the Distance in Rows between two Groups of Points.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. points_a : tuple | list | set
        2. points_b : tuple | list | set
    ============================================================================
     Return: float
    ============================================================================
    """
    assert type(points_a) in {tuple, list, set}
    assert type(points_b) in {tuple, list, set}
    li_x_a = [p.x for p in points_a]
    x_a = statistics.mean(li_x_a)
    li_x_b = [p.x for p in points_b]
    x_b = statistics.mean(li_x_b)
    return abs(x_a - x_b)


def distance_cols(points_a, points_b):
    """
    ============================================================================
     Description: Return the Distance in Columns between two Groups of Points.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. points_a : tuple | list | set
        2. points_b : tuple | list | set
    ============================================================================
     Return: float
    ============================================================================
    """
    assert type(points_a) in {tuple, list, set}
    assert type(points_b) in {tuple, list, set}
    li_y_a = [p.y for p in points_a]
    y_a = statistics.mean(li_y_a)
    li_y_b = [p.y for p in points_b]
    y_b = statistics.mean(li_y_b)
    return abs(y_a - y_b)
