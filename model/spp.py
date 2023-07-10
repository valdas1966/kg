from dataclasses import dataclass
from model.point import Point
from model.grid_blocks import GridBlocks
from f_utils import u_random


@dataclass
class SPP:
    grid: GridBlocks
    start: Point
    goal: Point

    @classmethod
    def generate_random(cls,
                        grid: GridBlocks,
                        n_spp: int = 1) -> list:
        """
        ============================================================================
         Desc: Return Random-SPP if n_spp=1, otherwise return List of Random-SPPs.
        ============================================================================
        """
        points = grid.points()
        pairs = u_random.to_groups(values=points, n=n_spp, k=2)
        res = [cls(grid, start, goal) for start, goal in pairs]
        return res
