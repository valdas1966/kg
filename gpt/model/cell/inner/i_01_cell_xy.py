
class CellXY:
    """
    ============================================================================
     Desc: Represents a Cell in a 2D-Grid.
           The Cell consists of (X,Y) Coordinates and an optional Name.
    ============================================================================
     Functionality:
    ----------------------------------------------------------------------------
        1. String Representation: The Cell is represented as "Name(X,Y)".
        2. Equality Logic: Two cells are equal if their (X,Y) match.
        3. Comparison Functions: Top-Left Cell < Bottom-Right Cell.
    ============================================================================
    """

    def __init__(self,
                 x: int,              # Cell's X-Coordinate
                 y: int,              # Cell's Y-Coordinate
                 name: str = None     # Optional Name for the Cell
                 ) -> None:
        """
        ========================================================================
         Desc: Init the Cell with its Position (X,Y) and an optional Name.
        ========================================================================
        """
        self.x = x
        self.y = y
        self.name = name

    def __str__(self) -> str:
        """
        ========================================================================
         Desc: Return a string representation of the Cell.
        ------------------------------------------------------------------------
            1. For cells with a name, the representation is "Name(x, y)".
            2. For cells without a name, the representation is "(x, y)".
        ========================================================================
        """
        name = self.name if self.name else str()
        return f'{name}({self.x},{self.y})'

    def __eq__(self,
               other: 'Cell'     # The other Cell to compare with
               ) -> bool:
        """
        ========================================================================
         Desc: Check if two cells are equal based on their X and Y coordinates.
        ========================================================================
        """
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: 'Cell') -> bool:
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __gt__(self, other: 'Cell') -> bool:
        return self.x > other.x or (self.x == other.x and self.y > other.y)

    def __le__(self, other: 'Cell') -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other: 'Cell') -> bool:
        return self.__gt__(other) or self.__eq__(other)
