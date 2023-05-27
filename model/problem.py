from dataclasses import dataclass
from point import Point


@dataclass
class Problem:
    domain: str
    map: str
    start: Point
    goals: set  # of Points


