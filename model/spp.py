from dataclasses import dataclass
from point import Point
from grid_blocks import GridBlocks


@dataclass
class SPP:
    domain: str
    map: str
    grid: GridBlocks
    start: Point
    goal: set
