from model.point_node import Node
from algo.astar_lookup import AStarLookup


class AStarLookupEarly(AStarLookup):
    """
    ============================================================================
     Description: A* Algorithm with Lookup Nodes (Perfect Heuristic to Goal).
    ============================================================================
    """

    def __init__(self, grid, start, goal, lookup=dict()):
        """
        ========================================================================
         Description: Init A* Algorithm
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. grid : Grid
            2. start : Point
            3. goal : Point
            4. lookup : Dict {point -> int (True-Distance to Goal)}
        ========================================================================
        """
        assert type(lookup) == dict
        super().__init__(grid, start, goal, lookup)

    def run(self):
        """
        ========================================================================
         Description: While the Search is not finished and the Opened is not
                        empty - Run the next move of the A* algorithm.
        ========================================================================
        """
        self.best = Node(self.start)
        self.best.update(father_cand=None, goal=self.goal)
        self.opened.push(self.best)
        while not self.opened.is_empty() and not self.is_found:
            self.next_move()

    def next_move(self):
        """
        ========================================================================
         Description: Run the next move of the Algorithm.
        ========================================================================
        """
        self.best = self.opened.pop()
        # print(self.start, self.goal, self.best)
        self.closed.add(self.best)
        if self.best == self.goal:
            self.is_found = True
        if self.best in self.lookup:
            self.is_found = True
            self.closed.remove(self.best)
        self.__expand()

    def __expand(self):
        """
        =======================================================================
         Description: Expand the Best.
        =======================================================================
        """
        points_neighbors = self.grid.neighbors(self.best)
        children = {point for point in points_neighbors} - self.closed
        for child in sorted(children):
            # Add Child into Opened if it is not there
            if self.opened.contains(child):
                child = self.opened.get(child)
            else:
                child = Node(child)
                self.opened.push(child)
            # Update Child if needed
            child.update(father_cand=self.best, goal=self.goal)
            # If Child in Lookup -> Set it's H-Value to be the True-Distance
            if child in self.lookup:
                child.set_h(self.lookup[child])
                child.is_lookup = True
                self.best = child
                self.is_found = True
                break
