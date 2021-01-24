import random
from collections import defaultdict


def random_pairs_by_distance(grid, amount, size=1):
    """
    ============================================================================
     Description: Return Dictionary with Pair of Points by their Distances.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks
        2. amount : int (Amount of Pairs)
        3. size : int (Size to Round the Distances)
    ============================================================================
     Return: dict {int -> list of tuple (Point_1, Point_2)}.
    ============================================================================
    """
    pairs = defaultdict(list)
    points = grid.points
    for i in range(amount):
        random.shuffle(points)
        point_a, point_b = points[:2]
        distance = point_a.distance(point_b)
        if size > 1:
            distance = (distance // size) * size
            pairs[distance].append((point_a, point_b))
    return pairs
