from f_utils import u_tester
from proj.ai.model.point import Point
from proj.ai.model.point_node import Node
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.logic.grid_blocks_ghf import LogicGridBlocksGHF


class TestLogicGridBlocksGHF:

    def __init__(self):
        u_tester.print_start(__file__)
        TestLogicGridBlocksGHF.__tester_to_dict_h()
        TestLogicGridBlocksGHF.__tester_to_dict_g()
        TestLogicGridBlocksGHF.__tester_to_dict_f()
        TestLogicGridBlocksGHF.__tester_true_distance()
        TestLogicGridBlocksGHF.__tester_to_nodes()
        TestLogicGridBlocksGHF.__tester_to_nodes_below_f()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_to_dict_h():
        grid = GridBlocks(rows=3)
        grid.set_block(x=1, y=1)
        goal = Point(2, 2)
        dict_h_test = LogicGridBlocksGHF.to_dict_h(grid, goal)
        dict_h_true = {Point(0, 0): 4, Point(0, 1): 3, Point(0, 2): 2,
                       Point(1, 0): 3, Point(1, 2): 1, Point(2, 0): 2,
                       Point(2, 1): 1, Point(2, 2): 0}
        p0 = dict_h_test == dict_h_true
        u_tester.run(p0)

    @staticmethod
    def __tester_to_dict_g():
        grid = GridBlocks(rows=3)
        grid.set_block(x=1, y=1)
        start = Point(0, 0)
        dict_g_test = LogicGridBlocksGHF.to_dict_g(grid, start)
        dict_g_true = {Point(0, 0): 0, Point(0, 1): 1, Point(0, 2): 2,
                       Point(1, 0): 1, Point(1, 2): 3, Point(2, 0): 2,
                       Point(2, 1): 3, Point(2, 2): 4}
        p0 = dict_g_test == dict_g_true
        u_tester.run(p0)

    @staticmethod
    def __tester_to_dict_f():
        grid = GridBlocks(rows=3)
        grid.set_block(x=1, y=1)
        start = Point(0, 0)
        goal = Point(2, 2)
        dict_f_test = LogicGridBlocksGHF.to_dict_f(grid, start, goal)
        dict_f_true = {Point(0, 0): 4, Point(0, 1): 4, Point(0, 2): 4,
                       Point(1, 0): 4, Point(1, 2): 4,
                       Point(2, 0): 4, Point(2, 1): 4, Point(2, 2): 4}
        p0 = dict_f_test == dict_f_true
        u_tester.run(p0)

    @staticmethod
    def __tester_true_distance():
        grid = GridBlocks(rows=3)
        grid.set_block(0, 1)
        point_a = Point(0, 0)
        points = {Point(0, 2), Point(2, 0)}
        distance_test = LogicGridBlocksGHF.true_distance(grid, point_a, points)
        distance_true = {Point(0, 2): 4, Point(2, 0): 2}
        p0 = distance_test == distance_true
        u_tester.run(p0)

    @staticmethod
    def __tester_to_nodes():
        grid = GridBlocks(rows=3)
        grid.set_block(Point(1, 1))
        start = Point(0, 0)
        goal = Point(2, 2)
        nodes_test = LogicGridBlocksGHF.to_nodes(grid, start, goal)
        points_true = [Point(2, 2), Point(1, 2), Point(2, 1), Point(0, 2),
                       Point(2, 0), Point(0, 1), Point(1, 0), Point(0, 0)]
        nodes_true = [Node(point) for point in points_true]
        p0 = nodes_test == nodes_true
        u_tester.run(p0)

    @staticmethod
    def __tester_to_nodes_below_f():
        grid = GridBlocks(rows=5)
        grid.set_block(Point(0, 1))
        grid.set_block(Point(1, 1))
        start = Point(0, 0)
        goal = Point(0, 2)
        nodes_f_test = LogicGridBlocksGHF.to_nodes_below_f(grid, start, goal)
        nodes_f_true = {Node(point) for point in [Point(0, 0), Point(1, 0)]}
        p0 = nodes_f_test == nodes_f_true
        u_tester.run(p0)


if __name__ == '__main__':
    TestLogicGridBlocksGHF()
