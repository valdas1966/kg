from model.point import Point
from model.grid import Grid
import statistics


def offsets(grid, points):
    """
    ============================================================================
     Description: Return the Offsets of the Point to the Grid-Borders.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : Grid
        2. points : Point | tuple | list | set
    ============================================================================
     Return: tuple of int (UP, RIGHT, DOWN, LEFT)
    ============================================================================
    """
    if type(points) == Point:
        points = [points]
    assert type(points) in {tuple, list, set}
    x = statistics.mean([p.x for p in points])
    y = statistics.mean([p.y for p in points])
    up = x
    right = grid.cols - y - 1
    down = grid.rows - x - 1
    left = y
    return up, right, down, left
