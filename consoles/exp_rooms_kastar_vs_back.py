import random
from f_utils import u_random
from f_utils import u_pickle
from f_utils import u_dict
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks_birooms import GridBlocksRooms
from proj.ai.algo.kastar_projection import KAStarProjection
from proj.ai.algo.astar_lookup import AStarLookup
from proj.ai.logic.point_distance import LogicPointDistance as lpd


dir_storage = 'G:\\Study\\Thesis\\Roni\\Rooms\\'
pickle_grids = dir_storage + 'grids.pickle'
pickle_start_goals = dir_storage + 'start_goals.pickle'
pickle_forward = dir_storage + 'forward.pickle'
pickle_backward = dir_storage + 'backward.pickle'
csv_report = dir_storage + 'report.csv'


def gen_grids(rows, cols, amount):
    """
    ==============================================================================
    Description: Generate Grids with two Rooms.
    ==============================================================================
    Arguments:
    ------------------------------------------------------------------------------
    1. rows : int (Rows in the Grid).
    2. cols : int (Cols in the Grid).
    3. amount : int (Amount of Grids to Generate).
    ==============================================================================
    """
    grids = set()
    for i in range(amount):
        is_valid = False
        while not is_valid:
            # Try Set Blocks
            row_block = u_random.get_random_int(2, 7)
            col_block = u_random.get_random_int(2, 7)
            if row_block + col_block < 9:
                continue
            corner = Point(row_block, col_block)
            # Set Door
            row_door, col_door = None, None
            is_row = u_random.get_random_int(0, 1)
            if is_row:
                row_door = u_random.get_random_int(0, row_block-1)
                col_door = col_block
            else:
                row_door = row_block
                col_door = u_random.get_random_int(0, col_block-1)
            door = Point(row_door, col_door)
            # Try Set Map
            grid = GridBlocksRooms(rows=rows, corner=corner, door=door,
                                   cols=cols)
            if grid in grids:
                continue
            grids.add(grid)
            is_valid = True
    u_pickle.dump(list(grids), pickle_grids)


def gen_start_goals():
    """
    ============================================================================
     Description: Generate Random Start and Goals Nodes.
    ============================================================================
     Pickle: List (100) of List (25*2*3) of Tuple (Point, List of Points).
    ============================================================================
    """
    grids = u_pickle.load(pickle_grids)
    start_goals_all = list()
    for i, grid in enumerate(grids):
        start_goals_grid = list()
        for j in range(25):
            left = grid.get_left_room()
            right = grid.get_right_room()
            # Start in Left Room
            random.shuffle(left)
            random.shuffle(right)
            start = left[0]
            for k in [2, 3, 5]:
                goals = right[:k]
                start_goals_grid.append((start, goals))
                print(i, j, k, 'left')
            # Start in Right Room
            random.shuffle(left)
            random.shuffle(right)
            start = right[0]
            for k in [2, 3, 5]:
                goals = left[:k]
                start_goals_grid.append((start, goals))
                print(i, j, k, 'right')
        start_goals_all.append(start_goals_grid)
        u_pickle.dump(start_goals_all, pickle_start_goals)


def gen_kastar_projective():
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    forward_all = list()
    for i, grid in enumerate(grids):
        forward_grid = list()
        li_start_goals = start_goals[i]
        for j, sg in enumerate(li_start_goals):
            start = sg[0]
            goals = sg[1]
            kastar = KAStarProjection(grid, start, goals)
            kastar.run()
            forward_grid.append(kastar)
            print(i, j)
        forward_all.append(forward_grid)
    u_pickle.dump(forward_all, pickle_forward)


def gen_back_astar_lookup():
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    backward_all = list()
    for i, grid in enumerate(grids):
        backward_grid = list()
        li_start_goals = start_goals[i]
        for j, sg in enumerate(li_start_goals):
            start = sg[0]
            goals = sg[1]
            goals = lpd.points_nearest(start, goals)
            astars = list()
            lookup = dict()
            for goal in goals:
                astar = AStarLookup(grid, goal, start, lookup)
                astar.run()
                lookup = u_dict.union(lookup, astar.lookup_goal())
                astars.append(astar)
            backward_grid.append(astars)
            print(i, j)
        backward_all.append(backward_grid)
    u_pickle.dump(backward_all, pickle_backward)


def gen_report():
    grids = u_pickle.load(pickle_grids)
    li_start_goals = u_pickle.load(pickle_start_goals)
    forwards = u_pickle.load(pickle_forward)
    backwards = u_pickle.load(pickle_backward)
    file = open(csv_report, 'w')
    file.write('map,experiment,goals,start_in_left,ratio_left_right,'
               'ratio_small_big,ratio_start_goals,'
               'distance_start_goals,distance_goals,distance_start_door,'
               'distance_goals_door,forward,backward,metric\n')
    for i, grid in enumerate(grids):
        left = len(grid.get_left_room())
        right = len(grid.get_right_room())
        ratio_left_right = round(left / right, 2)
        ratio_small_big = round(min(left, right) / max(left, right), 2)
        is_left = True
        counter = 0
        for j, kastar in enumerate(forwards[i]):
            start_in_left = int(is_left)
            ratio_start_goals = ratio_left_right
            if not start_in_left:
                ratio_start_goals = round(right / left, 2)
            counter += 1
            if counter == 3:
                counter = 0
                is_left = not is_left
            forward = len(kastar.closed)
            astars_back = backwards[i][j]
            closed_back = set()
            for astar in astars_back:
                closed_back.update(astar.closed)
            backward = len(closed_back)
            metric = round(1 - (backward / ((backward + forward) / 2)), 2)
            start_goals = li_start_goals[i][j]
            start = start_goals[0]
            goals = start_goals[1]
            distance_start_goals = lpd.distances_to(start, goals)
            distance_goals = lpd.distances(goals)
            distance_start_door = start.distance(grid.door)
            distance_goals_door = lpd.distances_to(grid.door, goals)
            file.write(f'{i},{j},{len(goals)},{start_in_left},'
                       f'{ratio_left_right},'
                       f'{ratio_small_big},'
                       f'{ratio_start_goals},{distance_start_goals},'
                       f'{distance_goals},{distance_start_door},'
                       f'{distance_goals_door},{forward},{backward},'
                       f'{metric}\n')
            print(i, j)
    file.close()


# gen_grids(rows=10, cols=10, amount=100)
# gen_start_goals()
# gen_kastar_projective()
# gen_back_astar_lookup()
gen_report()


"""
from f_excel.c_excel_map import ExcelMap
grids = u_pickle.load(pickle_grids)
grid = grids[11]
xl_map = ExcelMap(filename='G:\\Study\\Thesis\\Roni\\Rooms\\test_1.xlsx')
grid.draw_excel(xl_map=xl_map, row_start=62, col_start=2, with_numbers=True)
xl_map.close()


li_start_goals = u_pickle.load(pickle_start_goals)
print(li_start_goals[11][136])

forwards = u_pickle.load(pickle_forward)
kastar = forwards[76][45]
print(len(kastar.closed))

from proj.ai.algo.kastar_projection import KAStarProjection

kastar = KAStarProjection(grid, start, goals)
kastar.run()

backwards = u_pickle.load(pickle_backward)
astars = backwards[47][95]
for astar in astars:
    print(astar.start, astar.goal, astar.closed)
li_start_goals = u_pickle.load(pickle_start_goals)
print(li_start_goals[47][95])
"""