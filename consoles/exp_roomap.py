from f_utils import u_file
from f_utils import u_pickle
from f_utils.c_timer import Timer
from proj.ai.model.grid_blocks_roomap import GridBlocksRooMap
from proj.ai.algo.kastar_projection import KAStarProjection
from proj.ai.algo.kastar_backward import KAStarBackward
from proj.ai.algo.kastar_bi import KAStarBi


dir_results = 'D:\\Exp_RooMap\\10\\'
pickle_grids = dir_results + 'grids.pickle'
pickle_start_goals = dir_results + 'start_goals.pickle'
pickle_forward = dir_results + 'forward.pickle'
pickle_backward = dir_results + 'backward.pickle'
pickle_bi = dir_results + 'bi.pickle'
csv_times_forward = dir_results + 'times_forward.csv'
csv_times_backward = dir_results + 'times_backward.csv'
csv_times_bi = dir_results + 'times_bi.csv'


def get_size_room(path):
    if path[1].isdigit():
        return int(path[:2])
    return int(path[0])


def create_grids():
    dir_maps = 'D:\\Maps'
    grids = list()
    for filename in u_file.get_files_names(dir_maps):
        path = f'{dir_maps}\\{filename}'
        size_room = get_size_room(filename)
        grid = GridBlocksRooMap(path, size_room=size_room)
        grids.append(grid)
    u_pickle.dump(grids, pickle_grids)


def create_start_goals():
    start_goals = list()
    grids = u_pickle.load(pickle_grids)
    for grid in grids:
        epochs = list()
        for i in range(10):
            point_room_start, point_room_goals = grid.random_rooms(2)
            room_start = grid.get_room(point_room_start)
            start = room_start.points_random(amount=1)[0]
            start = grid.to_actual_point(start, point_room_start)
            room_goals = grid.get_room(point_room_goals)
            goals = room_goals.points_random(amount=10)
            goals = [grid.to_actual_point(goal, point_room_goals) for goal in
                     goals]
            epochs.append((start, goals))
        start_goals.append(epochs)
    u_pickle.dump(start_goals, pickle_start_goals)


def create_forward(k):
    li_forward = list()
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    file = open(csv_times_forward, 'w')
    file.write(f'map,experiment,seconds\n')
    for i, grid in enumerate(grids):
        epochs = list()
        for j, sg in enumerate(start_goals[i]):
            print(i, j)
            start, goals = sg
            timer = Timer()
            kastar = KAStarProjection(grid, start, goals[:k])
            file.write(f'{i},{j},{timer.elapsed()}\n')
            epochs.append(kastar)
        li_forward.append(epochs)
    file.close()
    u_pickle.dump(li_forward, pickle_forward)


def create_backward(k):
    li_backward = list()
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    file = open(csv_times_backward, 'w')
    file.write(f'map,experiment,seconds\n')
    for i, grid in enumerate(grids):
        epochs = list()
        for j, sg in enumerate(start_goals[i]):
            start, goals = sg
            timer = Timer()
            kastar = KAStarBackward(grid, start, goals[:k], lookup=dict())
            file.write(f'{i},{j},{timer.elapsed()}\n')
            epochs.append(kastar)
            print(i, j)
        li_backward.append(epochs)
    file.close()
    u_pickle.dump(li_backward, pickle_backward)


def create_bi(k):
    li_bi = list()
    grids = u_pickle.load(pickle_grids)
    start_goals = u_pickle.load(pickle_start_goals)
    file = open(csv_times_bi, 'w')
    file.write(f'map,experiment,seconds\n')
    for i, grid in enumerate(grids):
        epochs = list()
        for j, sg in enumerate(start_goals[i]):
            start, goals = sg
            timer = Timer()
            kastar = KAStarBi(grid, start, goals[:k])
            file.write(f'{i},{j},{timer.elapsed()}\n')
            epochs.append(kastar)
            print(i, j)
        li_bi.append(epochs)
    file.close()
    u_pickle.dump(li_bi, pickle_bi)


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


k = 10
# create_grids()
# create_start_goals()
create_forward(k)
create_backward(k)
create_bi(k)
# create_report()
