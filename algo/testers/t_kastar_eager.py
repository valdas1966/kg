from f_utils import u_tester
from algo.kastar_eager import KAStarEager
from algo.kastar_projection import KAStarProjection
from model.grid_blocks import GridBlocks
from model.point import Point


class TestKAStarEager:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_run()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_run():
        p0 = True
        for _ in range(100):
            grid = GridBlocks(rows=3, percent_blocks=20)
            start, goal_1, goal_2 = grid.points_random(amount=3)
            goals = {goal_1, goal_2}
            kastar_projection = KAStarProjection(grid, start, goals)
            kastar_projection.run()
            kastar_eager = KAStarEager(grid, start, goals)
            kastar_eager.run()
            p0 = kastar_projection.closed == kastar_eager.closed
            if not p0:
                break
        u_tester.run(p0)


if __name__ == '__main__':
    TestKAStarEager()
