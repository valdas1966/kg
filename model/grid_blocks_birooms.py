from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks


class GridBlocksBiRooms(GridBlocks):

    def __init__(self, rows, corner, door, cols=None):
        """
        ========================================================================
         Description: Constructor - Init Arguments.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. rows : int (Amount of Rows in the Map).
            2. cols : int (Amount of Columns in the Map).
            3. corner : Point (Corner of the Room).
            4. door : Point (Door of the Room).
        ========================================================================
        """
        if not cols:
            cols = rows
        assert type(rows) == int
        assert type(cols) == int
        assert type(corner) == Point
        assert type(door) == Point
        assert corner != door
        super().__init__(rows=rows, cols=cols)
        self.corner = corner
        self.door = door
        self.__set_walls()
        self.__set_door()

    def get_left_room(self):
        """
        ========================================================================
         Description: Return Points in the Left Room.
        ========================================================================
         Return : List of Point.
        ========================================================================
        """
        points = list()
        for row in range(self.rows):
            for col in range(self.cols):
                if row < self.corner.x and col < self.corner.y:
                    point = Point(row, col)
                    points.append(point)
        return points

    def get_right_room(self):
        """
        ========================================================================
         Description: Return Points in the Right Room.
        ========================================================================
         Return : List of Point.
        ========================================================================
        """
        points = list()
        for row in range(self.rows):
            for col in range(self.cols):
                if row > self.corner.x or col > self.corner.y:
                    point = Point(row, col)
                    points.append(point)
        return points

    def __set_walls(self):
        """
        ========================================================================
         Description: Build the Blocks in the Map that separates between Rooms.
        =======================================================================
        """
        # Block Column
        for x in range(self.corner.x):
            self.set_block(x=x, y=self.corner.y)
        # Block Row
        for y in range(self.corner.y):
            self.set_block(x=self.corner.x, y=y)
        # Block Corner
        self.set_block(self.corner)

    def __set_door(self):
        """
        ========================================================================
         Description: Build the Door in the Map.
        ========================================================================
        """
        self.set_value(value=0, point=self.door)

    def __hash__(self):
        """
        ========================================================================
         Description: Return Hash-Function with unique int for each Grid Rooms.
        ========================================================================
         Return : int (Hash Value).
        ========================================================================
        """
        h = str(self.corner.x) + str(self.corner.y) + \
            str(self.door.x) + str(self.door.y)
        return int(h)
