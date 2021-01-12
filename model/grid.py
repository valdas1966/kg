import numpy as np
import random
from proj.ai.model.point import Point


class Grid:

    def __init__(self, rows, cols=None):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. rows : int
            2. cols : int
        ========================================================================
        """
        self.rows = rows
        self.cols = cols or self.rows
        assert type(self.rows) == int
        assert type(self.cols) == int
        assert self.rows > 0
        assert self.cols > 0
        self.ndarray = np.zeros(shape=(self.rows, self.cols), dtype=int)

    def set_value(self, value, point=None, x=None, y=None):
        """
        ========================================================================
         Description: Set specific Value in the place of the Point.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. value : int
            2. point : Point
            3. x : int
            4. y : int
        ========================================================================
        """
        assert type(value) == int, f'type(value)={type(value)}'
        assert type(point) in [Point, type(None)], f'type(point)={type(point)}'
        if point:
            x = point.x
            y = point.y
        assert type(x) == int, f'type(x)={type(x)}, point={point}'
        assert type(y) == int, f'type(x)={type(y)}, point={point}'
        assert self.is_valid_point(Point(x, y), only_shape=True), Point(x, y)
        self.ndarray[x][y] = value

    def is_value(self, value, point=None, x=None, y=None):
        """
        ========================================================================
         Description: Return True if the Value exists in the specific Point.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. value : int
            2. point : Point
            3. x : int
            4. y : int
        ========================================================================
         Return: bool
        ========================================================================
        """
        if point:
            x = point.x
            y = point.y
        return self.ndarray[x][y] == value

    def points(self):
        """
        ========================================================================
         Description: Return List of Points in the Grid.
        ========================================================================
         Return: List of Points.
        ========================================================================
        """
        li = list()
        for x in range(self.rows):
            for y in range(self.cols):
                li.append(Point(x, y))
        return li

    def points_random(self, amount):
        """
        ========================================================================
         Description: Return List of Random Points in the Grid.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. amount : int
        ========================================================================
         Return: List of Points in the size of Amount.
        ========================================================================
        """
        points = self.points()
        random.shuffle(points)
        return points[:amount]

    def is_valid_point(self, point):
        """
        ========================================================================
         Description: Return True if the Point is Valid (in the Grid's Shape).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point : Point
        ========================================================================
         Return: bool
        ========================================================================
        """
        if point.x < 0:
            return False
        if point.x >= self.rows:
            return False
        if point.y < 0:
            return False
        if point.y >= self.cols:
            return False
        return True

    def neighbors(self, point):
        """
        ========================================================================
         Description: Return List of Valid Points (in the Shape of the Grid)
                        in the Point-Ordering (Up, Left, Right, Down).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point : Point
        ========================================================================
         Return: List of Points.
        ========================================================================
        """
        assert issubclass(type(point), Point), f'type(point)={type(point)}'
        points = list()

        def add_if_valid(p):
            if self.is_valid_point(p):
                points.append(p)

        add_if_valid(point.neighbor_up())
        add_if_valid(point.neighbor_left())
        add_if_valid(point.neighbor_right())
        add_if_valid(point.neighbor_down())

        return points

    def __eq__(self, other):
        """
        ========================================================================
         Description: Return True if the Grids of both Maps are equal.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : c_map
        ========================================================================
         Return : bool
        ========================================================================
        """
        if self.ndarray.shape == other.ndarray.shape:
            return (self.ndarray == other.ndarray).all()
        return False

    def __str__(self):
        """
        ========================================================================
         Description: Return str-representation of NDArray.
        ========================================================================
         Return: str
        ========================================================================
        """
        return str(self.ndarray)
