from collections import defaultdict
import random
from f_utils import u_file
from f_utils import u_pickle
from f_utils.c_timer import Timer
from proj.ai.model.grid_blocks_roomap import GridBlocksRooMap
from proj.ai.algo.kastar_projection import KAStarProjection
from proj.ai.algo.kastar_backward import KAStarBackward
from proj.ai.algo.kastar_bi import KAStarBi
from proj.ai.logic.point_distance import LogicPointDistance as logic


dir_results = 'D:\\Exp_RooMap_Equal\\'
pickle_grids = dir_results + 'grids.pickle'
pickle_start_goals = dir_results + 'start_goals.pickle'
pickle_start_goals_potential = dir_results + 'start_goals_potential.pickle'
csv_forward = dir_results + 'forward.csv'
csv_backward = dir_results + 'backward.csv'
csv_bi = dir_results + 'bi.csv'


def get_size_room(path):
    if path[1].isdigit():
        return int(path[:2])
    return int(path[0])


def create_grids():
    dir_maps = 'D:\\Maps'
    grids = defaultdict(list)
    for filename in u_file.get_files_names(dir_maps):
        path = f'{dir_maps}\\{filename}'
        size_room = get_size_room(filename)
        grid = GridBlocksRooMap(path, size_room=size_room)
        grids[size_room].append(grid)
    u_pickle.dump(grids, pickle_grids)


def create_start_goals_potential():
    start_goals = dict()
    grids = u_pickle.load(pickle_grids)
    for size in grids.keys():
        start_goals[size] = dict()
        for map, grid in enumerate(grids[size]):
            start_goals[size][map] = dict()
            start_goals[size][map][2] = defaultdict(set)
            start_goals[size][map][3] = defaultdict(set)
            start_goals[size][map][5] = defaultdict(set)
            start_goals[size][map][10] = defaultdict(set)
            for i in range(100000):
                point_room_start, point_room_goals = grid.random_rooms(2)
                room_start = grid.get_room(point_room_start)
                start = room_start.points_random(amount=1)[0]
                start = grid.to_actual_point(point=start,
                                             point_room=point_room_start)
                room_goals = grid.get_room(point_room_goals)
                goals = room_goals.points_random(amount=10)
                goals = [grid.to_actual_point(goal, point_room_goals) for goal
                         in goals]
                distance_2 = logic.distances_to(start, goals[:2])
                start_goals[size][map][2][distance_2].add((start,
                                                           tuple(goals[:2])))
                random.shuffle(goals)
                distance_3 = logic.distances_to(start, goals[:3])
                start_goals[size][map][3][distance_3].add((start,
                                                           tuple(goals[:3])))
                random.shuffle(goals)
                distance_5 = logic.distances_to(start, goals[:5])
                start_goals[size][map][5][distance_5].add((start,
                                                           tuple(goals[:5])))
                random.shuffle(goals)
                distance_10 = logic.distances_to(start, goals[:10])
                start_goals[size][map][10][distance_10].add((start,
                                                             tuple(goals[:10])))
                if not i % 1000:
                    print(size, f'{i:,}')
    u_pickle.dump(start_goals, pickle_start_goals_potential)


def create_start_goals():
    potential = u_pickle.load(pickle_start_goals_potential)
    sg = dict()
    for size, d_size in potential.items():
        sg[size] = dict()
        for map, d_map in d_size.items():
            sg[size][map] = dict()
            for k, d_k in d_map.items():
                sg[size][map][k] = defaultdict(list)
                for distance, set_sg in d_k.items():
                    sg[size][map][k][((distance // 100) * 100)+100].extend(
                        list(set_sg))
    sg_final = dict()
    for size, d_size in sg.items():
        sg_final[size] = dict()
        for map, d_map in d_size.items():
            sg_final[size][map] = dict()
            for k, d_k in d_map.items():
                if k not in {2, 10}:
                    continue
                sg_final[size][map][k] = defaultdict(list)
                for distance, set_sg in d_k.items():
                    li_sg = sg[size][map][k][distance]
                    random.shuffle(li_sg)
                    sg_final[size][map][k][distance] = li_sg[:5]
    u_pickle.dump(sg_final, pickle_start_goals)


def create_forward():
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    file = open(csv_forward, 'w')
    file.write(f'size,map,k,distance,i_sg,seconds,nodes\n')
    file.close()
    for size, d_size in start_goals.items():
        for map, d_map in d_size.items():
            for k, d_k in d_map.items():
                for distance, li_sg in d_k.items():
                    for i_sg, sg in enumerate(li_sg):
                        grid = grids[size][map]
                        start, goals = sg
                        timer = Timer()
                        kastar = KAStarProjection(grid, start, goals)
                        file = open(csv_forward, 'a')
                        file.write(f'{size},{map},{k},{distance},{i_sg},'
                                   f'{timer.elapsed()},{len(kastar.closed)}\n')
                        file.close()
                        print(size, map, k, distance, i_sg)


def create_backward():
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    file = open(csv_backward, 'w')
    file.write(f'size,map,k,distance,i_sg,seconds,nodes\n')
    file.close()
    for size, d_size in start_goals.items():
        for map, d_map in d_size.items():
            for k, d_k in d_map.items():
                for distance, li_sg in d_k.items():
                    for i_sg, sg in enumerate(li_sg):
                        grid = grids[size][map]
                        start, goals = sg
                        timer = Timer()
                        kastar = KAStarBackward(grid, start, goals,
                                                lookup=dict())
                        file = open(csv_backward, 'a')
                        file.write(f'{size},{map},{k},{distance},{i_sg},'
                                   f'{timer.elapsed()},'
                                   f'{sum(kastar.closed.values())}\n')
                        file.close()
                        print(size, map, k, distance, i_sg)


def create_bi():
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    file = open(csv_bi, 'w')
    file.write(f'size,map,k,distance,i_sg,seconds,nodes\n')
    file.close()
    for size, d_size in start_goals.items():
        for map, d_map in d_size.items():
            for k, d_k in d_map.items():
                for distance, li_sg in d_k.items():
                    for i_sg, sg in enumerate(li_sg):
                        grid = grids[size][map]
                        start, goals = sg
                        timer = Timer()
                        kastar = KAStarBi(grid, start, goals)
                        file = open(csv_bi, 'a')
                        file.write(f'{size},{map},{k},{distance},{i_sg},'
                                   f'{timer.elapsed()},'
                                   f'{sum(kastar.closed.values())}\n')
                        file.close()
                        print(size, map, k, distance, i_sg)


def create_report():
    li_forward = u_pickle.load(pickle_forward)
    li_backward = u_pickle.load(pickle_backward)
    li_bi = u_pickle.load(pickle_bi)
    csv_report = dir_results + 'report.csv'
    file = open(csv_report, 'w')
    file.write('map,experiment,forward,backward,bidirectional,oracle\n')
    for i in range(40):
        for j in range(10):
            forward = len(li_forward[i][j].closed)
            backward = sum(li_backward[i][j].closed.values())
            bi = sum(li_bi[i][j].closed.values())
            oracle = min(forward, backward, bi)
            file.write(f'{i},{j},{forward},{backward},{bi},{oracle}\n')
    file.close()


def test_1():
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    size = 64
    map = 9
    k = 10
    distance = 600
    i_sg = 0
    grid = grids[size][map]
    start, goals = start_goals[size][map][k][distance][i_sg]
    timer = Timer()
    kastar = KAStarBackward(grid, start, goals)
    print(f'{timer.elapsed()},{sum(kastar.closed.values())}')


#k = 10
# create_grids()
# create_valid_points_per_room()
# create_start_goals_potential()
# create_start_goals()
# create_forward()
# create_backward()
#create_bi()
# create_report()

test_1()
