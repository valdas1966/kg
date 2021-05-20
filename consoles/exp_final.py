from collections import defaultdict
import datetime
from algo.astar import AStar
from algo.kastar_projection import KAStarProjection
from algo.kastar_bi import KAStarBi
from algo.kastar_backward import KAStarBackward
from logic import u_grid_blocks
from logic import u_grid
from logic import u_points
from f_utils import u_file
from f_utils import u_pickle
from f_ds import u_df
import pandas as pd


dir_maps = 'd:\\temp\\maps\\'
dir_storage = 'd:\\temp\\final\\'
# dir_storage = 'g:\\roni\\model\\'
dir_forward = dir_storage + 'Forward\\'
pickle_grids = dir_storage + 'grids.pickle'
pickle_grids_final = dir_storage + 'grids_final.pickle'
pickle_pairs = dir_storage + 'pairs.pickle'
f_pickle_pairs = dir_storage + 'pairs_{0}.pickle'
f_pickle_sg = dir_storage + 'sg_{0}.pickle'
f_pickle_forward = dir_forward + '{0}_{1}_{2}_{3}_{4}.pickle'
csv_grids = dir_storage + 'grids.csv'
f_csv_pairs = dir_storage + 'pairs_{0}.csv'
csv_sg = dir_storage + 'sg.csv'
f_csv_found = dir_storage + 'found_{0}.csv'
f_csv_forward = dir_storage + 'forward_{0}.csv'
f_csv_bi = dir_storage + 'bi_{0}.csv'
f_csv_backward = dir_storage + 'backward_{0}.csv'
csv_results = dir_storage + 'results.csv'
csv_fe_raw = dir_storage + 'fe_raw.csv'
csv_fe_results = dir_storage + 'fe_results.csv'
csv_fe_dummies = dir_storage + 'fe_dummies.csv'
csv_train = dir_storage + 'train.csv'
csv_test = dir_storage + 'test.csv'

def create_grids():
    d_grids = defaultdict(dict)
    for filepath in u_file.filepaths(dir_maps):
        domain = filepath.split('\\')[-2]
        if domain not in d_grids:
            d_grids[domain] = defaultdict(dict)
        map = filepath.split('\\')[-1].replace('.map', '')
        grid = u_grid_blocks.from_map(filepath)
        d_grids[domain][map] = grid
        print(filepath, grid.rows, grid.cols, len(grid.points()))
    u_pickle.dump(d_grids, pickle_grids)


def print_grids():
    d_grids = u_pickle.load(pickle_grids)
    file = open(csv_grids, 'w')
    file.write('domain,map,rows,cols,nodes\n')
    for domain in d_grids:
        for map, grid in d_grids[domain].items():
            nodes = len(grid.points())
            file.write(f'{domain},{map},{grid.rows},{grid.cols},{nodes}\n')
            print(domain, map)
    file.close()


def create_grids_final():
    grids = u_pickle.load(pickle_grids)
    grids_final = dict()
    df = pd.read_csv(csv_grids)
    df = df[df['is_final'] == 1]
    for row in df.iterrows():
        domain = row[1]['domain']
        map = row[1]['map']
        if domain not in grids_final:
            grids_final[domain] = dict()
        grids_final[domain][map] = grids[domain][map]
    u_pickle.dump(grids_final, pickle_grids_final)


def grids_final_add_warcraft():
    domain = 'warcraft'
    d_grids = u_pickle.load(pickle_grids_final)
    d_grids[domain] = dict()
    for filepath in u_file.filepaths(dir_maps + '\\' + domain):
        map = filepath.split('\\')[-1].replace('.map', '')
        grid = u_grid_blocks.from_map(filepath)
        d_grids[domain][map] = grid
        print(filepath, grid.rows, grid.cols, len(grid.points()))
    u_pickle.dump(d_grids, pickle_grids_final)


def create_pairs(domain):
    d_pairs = dict()
    d_pairs[domain] = dict()
    d_grids = u_pickle.load(pickle_grids_final)
    for map, grid in d_grids[domain].items():
        pairs = u_grid_blocks.random_pairs_by_distance(grid,
                                                        amount=10000000,
                                                        size=100)
        d_pairs[domain][map] = pairs
        print(domain, map)
    u_pickle.dump(d_pairs, f_pickle_pairs.format(domain))


def print_pairs(domain):
    d_pairs = u_pickle.load(f_pickle_pairs.format(domain))
    file = open(f_csv_pairs.format(domain), 'w')
    file.write('domain,map,distance,pairs\n')
    for map in sorted(d_pairs[domain]):
        for distance in sorted(d_pairs[domain][map]):
            pairs = d_pairs[domain][map][distance]
            file.write(f'{domain},{map},{distance},{len(pairs)}\n')
    file.close()


def create_sg(domain):
    d_grids = u_pickle.load(pickle_grids)
    d_pairs_domain = u_pickle.load(f_pickle_pairs.format(domain))
    d_sg = dict()
    d_sg[domain] = dict()
    for i, map in enumerate(sorted(d_pairs_domain)):
        d_sg[domain][map] = dict()
        grid = d_grids[domain][map]
        for k in range(2, 11):
            d_sg[domain][map][k] = dict()
            for distance in sorted(d_pairs_domain[map]):
                if distance > 900:
                    continue
                pairs = d_pairs_domain[map][distance]
                li_sg = list()
                for (start, goal_a) in pairs:
                    goals = u_grid_blocks.random_points_radius(grid=grid,
                                                       point=goal_a,
                                                       radius=10,
                                                       amount=k-1)
                    if len(goals) == k-1:
                        goals.append(goal_a)
                        li_sg.append((start, goals))
                    if len(li_sg) == 12:
                        break
                d_sg[domain][map][k][distance] = li_sg
                print(domain, i, map, k, distance, len(li_sg))
    u_pickle.dump(d_sg, f_pickle_sg.format(domain))


def print_sg():
    def print_domain(file, pickle_sg):
        d_sg = u_pickle.load(pickle_sg)
        for domain in d_sg:
            for map in sorted(d_sg[domain]):
                for k in sorted(d_sg[domain][map]):
                    for distance in sorted(d_sg[domain][map][k]):
                        sg = len(d_sg[domain][map][k][distance])
                        file.write(f'{domain},{map},{k},{distance},{sg}\n')
    file = open(csv_sg, 'w')
    file.write('domain,map,k,distance,sg\n')
    print_domain(file, pickle_sg_mazes)
    print_domain(file, pickle_sg_random)
    print_domain(file, pickle_sg_rooms)
    file.close()


def print_found(domain):
    print('check_is_found', domain)
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    file = open(f_csv_found.format(domain), 'w')
    file.write('domain,map,k,distance,i,goal,found\n')
    file.close()
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    goal_0 = goals[0]
                    astar = AStar(grid, start, goal_0)
                    astar.run()
                    found = int(astar.is_found)
                    file = open(f_csv_found.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},'
                               f'{goal_0},{found}\n')
                    file.close()
                    for goal in goals[1:]:
                        astar = AStar(grid, goal_0, goal)
                        astar.run()
                        found = int(astar.is_found)
                        file = open(f_csv_found.format(domain), 'a')
                        file.write(f'{domain},{map},{k},{distance},{i},'
                                   f'{goal},{found}\n')
                        file.close()
                    print(datetime.datetime.now(), 'check', domain, map, k,
                          distance, i)


def create_forward(domain):
    print('forward', domain)
    file = open(f_csv_forward.format(domain), 'w')
    file.write('domain,map,k,distance,i,nodes\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    if not i == 11:
                        continue
                    kastar = KAStarProjection(grid, start, goals)
                    kastar.run()
                    pickle = f_pickle_forward.format(domain, map, k,
                                                     distance, i)
                    if not domain == 'mazes':
                        u_pickle.dump(kastar.closed, pickle)
                    nodes = len(kastar.closed)
                    file = open(f_csv_forward.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},{nodes}\n')
                    file.close()
                    print(datetime.datetime.now(), domain, map, k, distance, i)


def create_bi(domain):
    print('bi', domain)
    file = open(f_csv_bi.format(domain), 'w')
    file.write('domain,map,k,distance,i,nodes\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    if not i == 10:
                        continue
                    kastar = KAStarBi(grid, start, goals)
                    kastar.run()
                    nodes = sum(kastar.closed.values())
                    if not kastar.is_found:
                        nodes = -1
                    file = open(f_csv_bi.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},{nodes}\n')
                    file.close()
                    print(datetime.datetime.now(), domain, map, k, distance, i)


def create_backward(domain):
    print('backward', domain)
    file = open(f_csv_backward.format(domain), 'w')
    file.write('domain,map,k,distance,i,nodes\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    if not i == 10:
                        continue
                    kastar = KAStarBackward(grid, start, goals, lookup=dict())
                    kastar.run()
                    nodes = sum(kastar.closed.values())
                    if not kastar.is_found:
                        nodes = -1
                    file = open(f_csv_backward.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},{nodes}\n')
                    file.close()
                    print(datetime.datetime.now(), domain, map, k, distance, i)


def union_results():
    df_array = dict()
    for algo in {'forward', 'bi', 'backward'}:
        df_array[algo] = pd.DataFrame({'domain': [], 'map': [], 'k': [],
                               'distance': [], 'i': [], 'nodes': []})
        for domain in {'cities', 'games', 'mazes', 'random', 'rooms'}:
            for i in range(12):
                dir_results = f'{dir_storage}i {i}'
                csv = f'{dir_results}\\{algo}_{domain}.csv'
                df_cur = pd.read_csv(csv)
                df_array[algo] = df_array[algo].append(df_cur)
        df_array[algo] = df_array[algo].rename(columns={'nodes': algo})
        df_array[algo] = df_array[algo].drop_duplicates()
        df_array[algo].to_csv(f'{dir_storage}{algo}.csv')
    index = ['domain', 'map', 'k', 'distance', 'i']
    df_all = df_array['forward'].join(df_array['bi'].set_index(index), on=index)
    df_all = df_all.join(df_array['backward'].set_index(index), on=index)
    df_all.to_csv(f'{dir_storage}results.csv')


def create_fe_raw():
    u_file.write(csv_fe_raw, 'domain,map,k,i,distance,'
                             'distance_start_goals,distance_goals,'
                             'distance_rows,distance_cols,start_up,'
                             'start_right,start_down,start_left,goals_up,'
                             'goals_right,goals_down,goals_left\n')
    d_grids = u_pickle.load(pickle_grids)
    for domain in {'cities', 'games', 'mazes', 'random', 'rooms'}:
        d_sg = u_pickle.load(f_pickle_sg.format(domain))
        for map in sorted(d_sg[domain]):
            grid = d_grids[domain][map]
            for k in sorted(d_sg[domain][map]):
                for distance in sorted(d_sg[domain][map][k]):
                    li_sg = d_sg[domain][map][k][distance]
                    for i, (start, goals) in enumerate(li_sg):
                        distance_start_goals = u_points.distances_to(start, goals)
                        distance_goals = u_points.distances(goals)
                        distance_rows = u_points.distance_rows([start], goals)
                        distance_cols = u_points.distance_cols([start], goals)
                        offsets = u_grid.offsets(grid, start)
                        start_up, start_right, start_down, start_left = offsets
                        offsets = u_grid.offsets(grid, goals)
                        goals_up, goals_right, goals_down, goals_left = offsets
                        line_values = f'{domain},{map},{k},{i},{distance},' \
                                 f'{distance_start_goals},' \
                                 f'{distance_goals},{distance_rows},' \
                                 f'{distance_cols},{start_up},{start_right},' \
                                 f'{start_down},{start_left},{goals_up},' \
                                 f'{goals_right},{goals_down},{goals_left}\n'
                        u_file.append(csv_fe_raw, line_values)


def join_results_fe_raw():
    df_results = pd.read_csv(csv_results)
    df_fe_raw = pd.read_csv(csv_fe_raw)
    index = ['domain', 'map', 'k', 'distance', 'i']
    df_join = df_results.join(df_fe_raw.set_index(index), on=index)
    df_join = df_join.drop(df_join.columns[0], axis=1)
    df_join.to_csv(csv_fe_results)


def create_fe_dummies():
    df = pd.read_csv(csv_fe_results)
    df = pd.get_dummies(df)
    df = df.drop(df.columns[0], axis=1)
    df.to_csv(csv_fe_dummies)


def create_train_test():
    df = pd.read_csv(csv_fe_dummies)
    df_train, df_test = u_df.split_random(df, percent=75)
    df_train.to_csv(csv_train)
    df_test.to_csv(csv_test)


# create_grids()
# print_grids()
# create_grids_final()
# grids_final_add_warcraft()
# create_pairs('warcraft')
# print_pairs('warcraft')
# split_pairs()
# create_sg('cities')
# print_sg()
# create_forward('mazes')
# create_forward('random')
# create_forward('rooms')
# create_forward('games')
# create_forward('cities')
# create_bi('mazes')
# create_bi('random')
# create_bi('rooms')
# create_bi('games')
# create_bi('cities')
# create_backward('mazes')
# create_backward('random')
# create_backward('rooms')
# create_backward('games')
# create_backward('cities')
# union_results()
# create_fe_raw()
# join_results_fe_raw()
# create_fe_dummies()
create_train_test()
