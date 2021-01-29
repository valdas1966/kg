import random
import numpy as np
from collections import defaultdict
from model.point import Point
from model.grid_blocks import GridBlocks
from algo.astar import AStar


def sub_grid(grid, row_min, row_max, col_min, col_max):
    """
    ============================================================================
     Description: Return Sub-GridBlocks by Rows and Cols indexes.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks (The Big Grid)
        2. row_min : int
        3. row_max : int
        4. col_min : int
        5. col_max : int
    ============================================================================
     Return: GridBlocks (Sub-Grid of the Big-Grid).
    ============================================================================
    """
    assert type(grid) == GridBlocks
    assert type(row_min) == int
    assert type(row_max) == int
    assert type(col_min) == int
    assert type(col_max) == int
    assert row_min >= 0
    assert row_max < grid.rows
    assert col_min >= 0
    assert col_max < grid.cols
    ndarray = grid.ndarray[row_min:row_max+1, col_min:col_max+1]
    sub = GridBlocks(rows=row_max-row_min+1, cols=col_max-col_min+1)
    sub.ndarray = ndarray
    return sub


def sub_grid_radius(grid, point, radius):
    """
    ============================================================================
     Description: Return Sub-Grid by Point and Radius.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks (The Big Grid)
        2. point : Point
        3. Radius : int
    ============================================================================
     Return: GridBlocks (Sub-Grid of the Big-Grid).
    ============================================================================
    """
    assert type(grid) == GridBlocks
    assert type(point) == Point
    assert type(radius) == int
    assert radius >= 0
    row_min = max(0, point.x - radius)
    row_max = min(grid.rows-1, point.x + radius)
    col_min = max(0, point.y - radius)
    col_max = min(grid.cols - 1, point.y + radius)
    return sub_grid(grid, row_min, row_max, col_min, col_max)


def random_points_radius(grid, point, radius, amount):
    """
    ============================================================================
     Description: Return Random Points in Radius from a given Point.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks
        2. point : Point
        3. radius : int
        4. amount : int
    ============================================================================
     Return: list of Point.
    ============================================================================
    """
    assert type(grid) == GridBlocks
    assert type(point) == Point
    assert type(radius) == int
    assert type(amount) == int
    assert radius >= 0
    assert amount >= 0
    row_min = max(0, point.x - radius)
    col_min = max(0, point.y - radius)
    row_max = min(grid.rows-1, point.x + radius)
    col_max = min(grid.cols-1, point.y + radius)
    points = grid.points_random(amount+1, row_min, col_min, row_max, col_max)
    if point in points:
        points.remove(point)
    return points[:amount]


def is_clean_line(grid, point_a, point_b):
    """
    ============================================================================
     Description: Return True if there is a Clean Line between the Points
                    (no obstacles on the airline)
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks
        2. point_a : Point
        3. point_b : Point
    ============================================================================
     Return: bool
    ============================================================================
    """
    assert type(grid) == GridBlocks
    assert type(point_a) == Point
    assert type(point_b) == Point
    astar = AStar(grid, point_a, point_b)
    astar.run()
    return len(astar.optimal_path()) == point_a.distance(point_b)+1


def are_clean_lines(grid, points):
    """
    ============================================================================
     Description: Return True if there are Clean-Lines between all the Points.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks
        2. points : Set of Point
    ============================================================================
     Return: bool
    ============================================================================
    """
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            if not is_clean_line(grid, p1, p2):
                return False
    return True


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
    assert type(grid) == GridBlocks
    assert type(amount) == int
    assert type(size) == int
    pairs = defaultdict(list)
    points = grid.points()
    for i in range(amount):
        j = i % len(points)
        if not j:
            random.shuffle(points)
        j_first = j * 2
        j_last = j_first + 2
        if j_last > len(points):
            continue
        point_a, point_b = points[j_first:j_last]
        distance = point_a.distance(point_b)
        if size > 1:
            distance = (distance // size) * size
            pairs[distance].append((point_a, point_b))
    return pairs


def random_satellites(grid, point, radius, amount, epochs=0):
    """
    ============================================================================
     Description: Return List of Satellite-Points with Clean-Line to a
                    given Point.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks
        2. point : Point (Given Point)
        3. radius : int (Max Radius for Satellite)
        4. amount : int (Amount of Satellites)
        5. epochs : int (Epochs to try. Epochs>0 -> must be Clean-Line)
    ============================================================================
     Return: list of Point (empty list on fail).
    ============================================================================
    """
    assert type(grid) == GridBlocks
    assert type(point) == Point
    assert type(radius) == int
    assert type(amount) == int
    assert type(epochs) == int
    satellites = random_points_radius(grid, point, radius, amount)
    is_valid = are_clean_lines(grid, satellites)
    while epochs and not is_valid:
        satellites = random_points_radius(grid, point, radius, amount)
        is_valid = are_clean_lines(grid, satellites)
        epochs -= 1
    if not is_valid:
        return list()
    return satellites


def from_map(path, char_valid='.', rows_pass=4):
    """
    ============================================================================
     Description: Generate GridBlocks from Map-File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to Map-File).
        2. char_valid : str (Char that indicates Valid-Point in the Map).
        3. rows_pass : int (Number of First-Rows to Pass (meta-data)).
    ============================================================================
     Return: GridBlocks (Generated from the Map-File).
    ============================================================================
    """
    rows = list()
    file = open(path, 'r')
    lines = file.readlines()[rows_pass:]
    for line in lines:
        row = list(line.strip())
        row = [0 if x == char_valid else -1 for x in row]
        rows.append(row)
    file.close()
    ndarray = np.array(rows)
    grid = GridBlocks(rows=ndarray.shape[0], cols=ndarray.shape[1])
    grid.ndarray = ndarray
    return grid
