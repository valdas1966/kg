from dataclasses import dataclass
from logic import u_grid_blocks
from model.grid_domain_map import GridDomainMap
from model.point import Point
from model.spp import SPP


cache = dict()


@dataclass(frozen=True)
class KSPP:
    grid: GridDomainMap
    start: Point
    goals: tuple

    @property
    def k(self):
        return len(self.goals)

    def __hash__(self):
        return hash((self.grid, self.start, tuple(self.goals)))

    @staticmethod
    def enhance_goals(grid: GridDomainMap,
                      goal: Point,
                      k: int,
                      radius: int) -> list:
        """
        ========================================================================
         Desc: Return List of Enhanced-Goals
                      (Goal + Additional [k-1] Goals in [radius].
        ========================================================================
        """
        goals = u_grid_blocks.random_points_radius(grid=grid,
                                                   point=goal,
                                                   radius=radius,
                                                   amount=k-1)
        goals.append(goal)
        return goals

    @classmethod
    def generate_random(cls,
                        grid: GridDomainMap,
                        n: int,
                        k: int,
                        radius: int) -> set:
        """
        ========================================================================
         Desc: Return Random [n] generated [k]-SPPs when goals are in [radius].
        ========================================================================
        """
        kspps = set()
        while len(kspps) < n:
            spp = SPP.generate_random(grid, n_spp=1)[0]
            goals = KSPP.enhance_goals(grid=grid,
                                       goal=spp.goal,
                                       k=k,
                                       radius=radius)
            if len(goals) < k:
                continue
            kspp = KSPP(grid, spp.start, goals)
            kspps.add(kspp)
        return kspps

    def to_meta(self) -> tuple:
        return self.grid.domain, \
               self.grid.map, \
               self.grid.path, \
               self.start, \
               self.goals

    @classmethod
    def from_meta(cls,
                  domain: str,
                  map: str,
                  path: str,
                  start: Point,
                  goals: tuple):
        if path in cache:
            grid = cache[path]
        else:
            grid = GridDomainMap(domain, map, path)
            cache[path] = grid
        return KSPP(grid, start, goals)
