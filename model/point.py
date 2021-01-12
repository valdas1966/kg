import math
from f_const.directions import Directions


class Point:

    def __init__(self, x, y=None):
        if type(x) == Point:
            x = x.x
            y = x.y
        assert type(x) == int, print(type(x))
        assert type(y) == int
        self.x = x
        self.y = y

    def distance(self, other):
        """
        ========================================================================
         Description: Return Manhattan-Distance between Self and Other Points.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. other : Point.
        ========================================================================
         Return: int.
        ========================================================================
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbor_up(self):
        return Point(self.x-1, self.y)

    def neighbor_down(self):
        return Point(self.x+1, self.y)

    def neighbor_left(self):
        return Point(self.x, self.y-1)

    def neighbor_right(self):
        return Point(self.x, self.y+1)

    def __str__(self):
        """
        ========================================================================
         Description: Return str-representation of the Point.
        ========================================================================
         Return: str in format of (Point.x, Point.y)
        ========================================================================
        """
        return f'({self.x},{self.y})'

    def __repr__(self):
        """
        ========================================================================
         Description: Return str-representation of the Point.
        ========================================================================
         Return: str in format of (Point.x, Point.y)
        ========================================================================
        """
        return self.__str__()

    def __eq__(self, other):
        """
        ========================================================================
         Description: Return True if Self is equal to Other.
        ========================================================================
            1. other : Point
        ========================================================================
         Return : Boolean
        ========================================================================
        """
        if other is None:
            return False
        assert issubclass(type(other), Point), f'type(other)={type(other)}'
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """
        ========================================================================
         Description: Return True if Self is not equal to Other.
        ========================================================================
            1. other : Point
        ========================================================================
         Return : Boolean
        ========================================================================
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        ========================================================================
         Description: Return True if Self is less than Other.
        ========================================================================
            1. other : Point
        ========================================================================
         Return : Boolean
        ========================================================================
        """
        if self.x < other.x:
            return True
        if self.x == other.x:
            if self.y < other.y:
                return True
        return False

    def __le__(self, other):
        """
        ========================================================================
         Description: Return True if Self is less or equal to Other.
        ========================================================================
            1. other : Point
        ========================================================================
         Return : Boolean
        ========================================================================
        """
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        """
        ========================================================================
         Description: Return True if Self is great than Other.
        ========================================================================
            1. other : Point
        ========================================================================
         Return : Boolean
        ========================================================================
        """
        return not self.__le__(other)

    def __ge__(self, other):
        """
        ========================================================================
         Description: Return True if Self is great or equal to Other.
        ========================================================================
            1. other : Point
        ========================================================================
         Return : Boolean
        ========================================================================
        """
        return not self.__lt__(other)

    def __hash__(self):
        """
        ========================================================================
         Description: Return Hash-Value of the Point.
        ========================================================================
         Return: int
        ========================================================================
        """
        return self.x * 1000000 + self.y

    @classmethod
    def direction(cls, p1, p2):
        """
        ============================================================================
         Description: Return the Direction from Point_1 to Point_2 in Degrees.
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1. p1 : Point.
            2. p2 : Point
        ============================================================================
         Return: float (Degree from 0 to 360).
        ============================================================================
        """
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        res = math.atan2(dx*(-1), dy*(-1)) / math.pi * 180
        if res < 0:
            res += 360
        return res

    @classmethod
    def compass_direction(cls, p1, p2):
        """
        ============================================================================
         Description: Return Compass Direction from Point_1 to Point_2.
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1. p1 : Point.
            2. p1 : Point.
        ============================================================================
         Return: Directions { UP | RIGHT | DOWN | LEFT }.
        ============================================================================
        """
        d = Point.direction(p1, p2)
        if d >= 315 or d <= 45:
            return Directions.UP
        if 45 <= d <= 135:
            return Directions.RIGHT
        if 135 <= d <= 225:
            return Directions.DOWN
        if 225 <= d <= 315:
            return Directions.LEFT

