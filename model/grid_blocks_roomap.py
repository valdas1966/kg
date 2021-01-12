import numpy as np
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks


class GridBlocksRooMap(GridBlocks):

    def __init__(self, path, size_room, char_valid='.', rows_pass=4,
                 goals_in_room_max=10):
        """
        ========================================================================
         Description: Create Grid of Room-Map based on Map-File.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. path : str (Path to Map-File).
            2. size_room : int (Edge of the Room (Square)).
            3. char_valid : str (Char that represents Valid Point).
            4. rows_pass : int (Meta-Data rows on the top of the file).
            5. goals_in_room_max : int (Max Number of Goals in the Room).
        ========================================================================
        """
        self.size_room = size_room
        self.goals_in_room_max = goals_in_room_max
        rows = list()
        file = open(path, 'r')
        lines = file.readlines()[rows_pass:]
        for line in lines:
            row = list(line.strip())
            row = [0 if x == char_valid else -1 for x in row]
            rows.append(row)
        file.close()
        ndarray = np.array(rows)
        super().__init__(rows=ndarray.shape[0], cols=ndarray.shape[1])
        self.ndarray = ndarray
        self.rows_room = int(self.rows / self.size_room)
        self.cols_room = int(self.cols / self.size_room)
        self.rooms = GridBlocks(rows=self.rows_room, cols=self.cols_room)
        self.__set_rooms()

    def get_room(self, row_room, col_room=None):
        """
        ========================================================================
         Description: Return Grid that represents Room by its Row and Col.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. row_room : int or Point
            2. col_room : int
        ========================================================================
         Return: GridBlcoks
        ========================================================================
        """
        if type(row_room) == Point:
            row_room, col_room = row_room.x, row_room.y
        assert type(row_room) == int
        assert type(col_room) == int
        assert self.rooms.is_valid_point(Point(row_room, col_room))
        row_a = row_room * self.size_room
        row_b = (row_room + 1) * self.size_room
        col_a = col_room * self.size_room
        col_b = (col_room + 1) * self.size_room
        ndarray = self.ndarray[row_a:row_b, col_a:col_b]
        grid = GridBlocks(rows=self.size_room, cols=self.size_room)
        grid.ndarray = ndarray
        return grid

    def get_point_room(self, point):
        """
        ========================================================================
         Description: Return Point (Room-Representation) of given Point in Map.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. point : Point
        ========================================================================
         Return: Point (Room-Representation)
        ========================================================================
        """
        assert type(point) == Point
        x = point.x // self.size_room
        y = point.y // self.size_room
        return Point(x, y)

    def random_rooms(self, amount):
        """
        ========================================================================
         Description: Return List of N-Random Points each represent
                        a Random-Room from the RooMap.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. amount : int (Amount of Random-Rooms to return).
        ========================================================================
         Return: list of Point.
        ========================================================================
        """
        return self.rooms.points_random(amount)

    def to_actual_point(self, point, point_room):
        """
        ========================================================================
         Description: Convert Room-Address (represented by Point) and
                        relatively in-room Point-Location into real
                        Point coordinates.
        ========================================================================
            1. point : Point (Relative Point to Convert).
            2. point_room : Point (Point that represents a Room).
        ========================================================================
         Return: Point
        ========================================================================
        """
        assert type(point) == Point
        assert type(point_room) == Point
        x = point.x + (point_room.x * self.size_room)
        y = point.y + (point_room.y * self.size_room)
        return Point(x, y)

    def __set_rooms(self):
        """
        ========================================================================
         Description: Set Grid of Rooms (each Point represents a Room in Map).
        ========================================================================
        """
        for row_room in range(self.rows_room):
            for col_room in range(self.cols_room):
                room = self.get_room(row_room, col_room)
                if len(room.points()) < self.goals_in_room_max:
                    self.rooms.set_block(row_room, col_room)
