from proj.ai.model.grid import Grid
from proj.ai.model.point import Point
import random


class GridBlocks(Grid):

    BLOCK = -1

    def __init__(self, rows, cols=None, percent_blocks=0):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. rows : int
            2. cols : int
            3. percent_blocks : int [0:100]
        ========================================================================
        """
        assert type(rows) == int
        assert type(percent_blocks) == int
        super().__init__(rows, cols)
        self.percent_blocks = percent_blocks
        self.__set_random_blocks()

    def set_block(self, x, y=None):
        """
        ========================================================================
         Description: Set Block (value = -1) in the Map.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. x : int (or Point)
            2. y : int (or None)
        ========================================================================
        """
        if type(x) == Point:
            x, y = x.x, x.y
        assert type(x) == int and type(y) == int
        assert super().is_valid_point(Point(x, y))
        self.set_value(value=self.BLOCK, x=x, y=y)

    def is_block(self, point=None, x=None, y=None):
        """
        ========================================================================
         Description: Return True if the Point is Block in the Map.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point : Point
            2. x : int
            3. y : int
        ========================================================================
         Return : bool
        ========================================================================
        """
        return self.is_value(value=self.BLOCK, point=point, x=x, y=y)

    def is_valid_points(self, points, only_shape=False):
        for point in points:
            if not self.is_valid_point(point, only_shape):
                return False
        return True

    def is_valid_point(self, point, only_shape=False):
        """
        ========================================================================
         Description: Return True if Point is not Block.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point : Point
            2. only_shape : bool
        ========================================================================
         Return: bool
        ========================================================================
        """
        if only_shape:
            return super().is_valid_point(point)
        return super().is_valid_point(point) and not self.is_block(point)

    def points(self):
        """
        ========================================================================
         Description: Return List of Valid Points in the Grid (not blocks).
        ========================================================================
         Return: List of Points.
        ========================================================================
        """
        return [p for p in super().points() if self.is_valid_point(p)]

    def points_random(self, amount):
        """
        ========================================================================
         Description: Return List of Random Valid Points in the Grid.
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

    def neighbors(self, point):
        """
        ========================================================================
         Description: Return Valid Neighbors.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point : Point
        ========================================================================
         Return: List of Points in Point-Ordering (Up, Left, Right, Down).
        ========================================================================
        """
        assert issubclass(type(point), Point), f'type(point)={type(point)}'
        return [p for p in super().neighbors(point) if self.is_valid_point(p)]

    def blocks(self):
        """
        ========================================================================
         Description: Return List of Points that represents Blocks in the Grid.
        ========================================================================
         Return: List of Points.
        ========================================================================
        """
        return set(super().points()) - set(self.points())

    def draw_excel(self, xl_map, row_start, col_start, title=str(),
                   with_numbers=False):
        # Draw the Title
        xl_map.set_blocks(row=row_start, col=col_start, cols=self.cols+2)
        xl_map.set_value(row=row_start, col=col_start+1, value=title)
        xl_map.set_font(row=row_start, col=col_start+1,
                        color='FFFFFF', is_bold=True)
        xl_map.merge_cells(row=row_start, col=col_start + 1, cols=self.cols)
        # Draw the Map
        for block in self.blocks():
            xl_map.set_blocks(row_start+block.x+2, col_start+block.y+1)
        # Draw Top Border
        xl_map.set_blocks(row=row_start+1, col=col_start, cols=self.cols+2)
        # Draw Bottom Border
        xl_map.set_blocks(row=row_start+self.rows+2, col=col_start,
                          cols=self.cols+2)
        # Draw Left Border
        xl_map.set_blocks(row=row_start+2, col=col_start, rows=self.rows)
        # Draw Right Border
        xl_map.set_blocks(row=row_start+2, col=col_start+self.cols+1,
                          rows=self.rows)
        if with_numbers:
            # Left Numbers
            for i, row in enumerate(range(row_start+2, row_start+self.rows+2)):
                xl_map.set_value(row, col_start, value=i)
            # Top Numbers
            for i, col in enumerate(range(col_start+1, col_start+self.cols+1)):
                xl_map.set_value(row_start+1, col, value=i)

    def __set_random_blocks(self):
        """
        ========================================================================
         Description: Set Random Blocks to the Grid by the Percent_Blocks.
        ========================================================================
        """
        len_blocks = int(self.rows * self.cols * self.percent_blocks / 100)
        if not len_blocks:
            return
        points_blocks = self.points_random(len_blocks)
        for point in points_blocks:
            self.set_block(point)
