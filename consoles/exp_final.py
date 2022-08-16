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
from f_data_science import u_df
from f_data_science import u_rfr
import pandas as pd
from sklearn.model_selection import GridSearchCV


dir_maps = 'd:\\temp\\maps\\'
dir_storage = 'd:\\temp\\final\\'
#dir_storage = 'g:\\roni\\model\\'
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
f_csv_regret = dir_storage + 'regret_{0}.csv'
csv_results = dir_storage + 'results.csv'
# csv_results_best = dir_storage + 'results_best.csv'
csv_fe_raw = dir_storage + 'fe_raw.csv'
f_csv_fe_raw = dir_storage + 'fe_raw_{0}.csv'
csv_fe_results = dir_storage + 'fe_results.csv'
csv_fe_dummies = dir_storage + 'fe_dummies.csv'
f_csv_x_train = dir_storage + 'x_train_{0}.csv'
f_csv_y_train = dir_storage + 'y_train_{0}.csv'
f_csv_x_test = dir_storage + 'x_test_{0}.csv'
f_csv_y_test = dir_storage + 'y_test_{0}.csv'
f_pickle_model = dir_storage + 'model_{0}.pickle'
f_csv_pred = dir_storage + 'pred_{0}.csv'
f_csv_optimal = dir_storage + 'optimal_{0}.csv'

maps_train = {'ost000t', 'ost100d', 'random512-30-7', 'random512-35-2',
              'Paris_1_1024', 'Paris_2_1024', '8room_004', '8room_008',
              'maze512-8-0', 'maze512-8-5'}


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


"""
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
"""

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

def create_optimal(domain):
    print('optimal', domain)
    file = open(f_csv_optimal.format(domain), 'w')
    file.write('domain,map,k,distance,i,optimal,forward\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    kastar = KAStarProjection(grid, start, goals)
                    kastar.run()
                    forward = len(kastar.closed)
                    optimal_nodes = set()
                    for li in kastar.optimal_paths.values():
                        optimal_nodes.update(set(li))
                    optimal = len(optimal_nodes)
                    file = open(f_csv_optimal.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},{optimal},'
                               f'{forward}\n')
                    file.close()
                    print(datetime.datetime.now(), domain, map, k, distance, i)


def create_forward_mazes():
    domain = 'mazes'
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    pickle = f_pickle_forward.format(domain, map, k,
                                                     distance, i)
                    if u_file.is_exists(pickle):
                        continue
                    kastar = KAStarProjection(grid, start, goals)
                    kastar.run()
                    u_pickle.dump(kastar.closed, pickle)
                    print(datetime.datetime.now(), domain, map, k, distance, i)


def create_regret(domain):
    print('regret', domain)
    file = open(f_csv_regret.format(domain), 'w')
    file.write('domain,map,k,distance,i,first_h,first_g,first_closed,'
               'first_opened\n')
    file.close()
    d_grids = u_pickle.load(pickle_grids_final)
    d_sg = u_pickle.load(f_pickle_sg.format(domain))
    for map in sorted(d_sg[domain]):
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    goal = list(u_points.nearest(start, goals).keys())[0]
                    astar = AStar(grid, start, goal)
                    astar.run()
                    first_h = start.distance(goal)
                    first_g = astar.best.g
                    first_closed = len(astar.closed)
                    first_opened = len(astar.opened._opened)
                    file = open(f_csv_regret.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},{first_h},'
                               f'{first_g},{first_closed},{first_opened}\n')
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
        #for domain in {'cities', 'games', 'mazes', 'random', 'rooms'}:
        for domain in {'mazes', 'random', 'rooms'}:
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
    df_all.to_csv(csv_results)


def create_fe_raw(domain):
    titles = 'domain,map,k,i,distance,rows,cols,points_valid,' \
             'distance_start_goals,distance_start_goals_points_valid,' \
             'distance_start_goals_rows,distance_start_goals_rows_rows,' \
             'distance_start_goals_cols,distance_start_goals_cols_cols,' \
             'distance_goals,distance_goals_points_valid,' \
             'start_up,start_up_rows,start_right,start_right_cols,' \
             'start_down,start_down_rows,start_left,start_left_cols,' \
             'goals_up,goals_up_rows,goals_right,goals_right_cols,' \
             'goals_down,goals_down_rows,goals_left,goals_left_cols\n'
    u_file.write(f_csv_fe_raw.format(domain), titles)
    d_grids = u_pickle.load(pickle_grids)
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
                    li_features = list()
                    li_features.append(domain)
                    li_features.append(map)
                    li_features.append(k)
                    li_features.append(i)
                    li_features.append(distance)
                    li_features.append(grid.rows)
                    li_features.append(grid.cols)
                    li_features.append(len(grid.points()))
                    li_features.append(distance_start_goals)
                    li_features.append(round(distance_start_goals/len(
                        grid.points()), 2))
                    li_features.append(distance_goals)
                    li_features.append(round(distance_goals/len(
                        grid.points()), 2))
                    li_features.append(distance_rows)
                    li_features.append(round(distance_rows/grid.rows, 2))
                    li_features.append(distance_cols)
                    li_features.append(round(distance_cols/grid.cols, 2))
                    li_features.append(start_up)
                    li_features.append(round(start_up/grid.rows, 2))
                    li_features.append(start_right)
                    li_features.append(round(start_right/grid.cols, 2))
                    li_features.append(start_down)
                    li_features.append(round(start_down/grid.rows, 2))
                    li_features.append(start_left)
                    li_features.append(round(start_left/grid.cols, 2))
                    li_features.append(goals_up)
                    li_features.append(round(goals_up / grid.rows, 2))
                    li_features.append(goals_right)
                    li_features.append(round(goals_right / grid.cols, 2))
                    li_features.append(goals_down)
                    li_features.append(round(goals_down / grid.rows, 2))
                    li_features.append(goals_left)
                    li_features.append(round(goals_left / grid.cols, 2))
                    li_features = [str(x) for x in li_features]
                    line_values = f'{",".join(li_features)}\n'
                    u_file.append(f_csv_fe_raw.format(domain), line_values)
                    print(domain, map, k, distance, i)


def union_fe_raw():
    df = pd.read_csv(f_csv_fe_raw.format('cities'))
    df = df.append(pd.read_csv(f_csv_fe_raw.format('games')))
    df = df.append(pd.read_csv(f_csv_fe_raw.format('mazes')))
    df = df.append(pd.read_csv(f_csv_fe_raw.format('random')))
    df = df.append(pd.read_csv(f_csv_fe_raw.format('rooms')))
    df.to_csv(csv_fe_raw, index=False)


def join_results_fe_raw():
    df_results = pd.read_csv(csv_results)
    df_fe_raw = pd.read_csv(csv_fe_raw)
    index = ['domain', 'map', 'k', 'distance', 'i']
    df_join = df_results.join(df_fe_raw.set_index(index), on=index)
    df_join = df_join.drop(df_join.columns[0], axis=1)
    df_join.to_csv(csv_fe_results, index=False)


def create_fe_dummies():
    df = pd.read_csv(csv_fe_results)
    df = pd.get_dummies(df)
    df = df.drop(['distance', 'i'], axis=1)
    df.to_csv(csv_fe_dummies, index=False)


def create_fe_dummies_map():
    df = pd.read_csv(csv_fe_results)
    df = pd.get_dummies(df, columns=['domain'])
    df = df.drop(['distance', 'i'], axis=1)
    df.to_csv(csv_fe_dummies, index=False)


def create_train_test():
    df = pd.read_csv(csv_fe_dummies)
    cols_features = list(df.columns)
    cols_features.remove('forward')
    cols_features.remove('bi')
    cols_features.remove('backward')
    df_train, df_test = u_df.split_random(df, percent=75)
    df_train_forward = df_train.drop(['bi', 'backward'], axis=1)
    x_train_forward, y_train_forward = u_df.split_to_x_y(df_train_forward,
                                                         cols_features,
                                                         col_label='forward')
    df_test_forward = df_test.drop(['bi', 'backward'], axis=1)
    x_test_forward, y_test_forward = u_df.split_to_x_y(df_test_forward,
                                                       cols_features,
                                                       col_label='forward')
    df_train_bi = df_train.drop(['forward', 'backward'], axis=1)
    x_train_bi, y_train_bi = u_df.split_to_x_y(df_train_bi,
                                               cols_features,
                                               col_label='bi')
    df_test_bi = df_test.drop(['forward', 'backward'], axis=1)
    x_test_bi, y_test_bi = u_df.split_to_x_y(df_test_bi,
                                             cols_features,
                                             col_label='bi')
    df_train_backward = df_train.drop(['forward', 'bi'], axis=1)
    x_train_backward, y_train_backward = u_df.split_to_x_y(df_train_backward,
                                                           cols_features,
                                                           col_label='backward')
    df_test_backward = df_test.drop(['forward', 'bi'], axis=1)
    x_test_backward, y_test_backward = u_df.split_to_x_y(df_test_backward,
                                                         cols_features,
                                                         col_label='backward')
    x_train_forward.to_csv(f_csv_x_train.format('forward'), index=False)
    y_train_forward.to_csv(f_csv_y_train.format('forward'), index=False)
    x_test_forward.to_csv(f_csv_x_test.format('forward'), index=False)
    y_test_forward.to_csv(f_csv_y_test.format('forward'), index=False)
    x_train_bi.to_csv(f_csv_x_train.format('bi'), index=False)
    y_train_bi.to_csv(f_csv_y_train.format('bi'), index=False)
    x_test_bi.to_csv(f_csv_x_test.format('bi'), index=False)
    y_test_bi.to_csv(f_csv_y_test.format('bi'), index=False)
    x_train_backward.to_csv(f_csv_x_train.format('backward'), index=False)
    y_train_backward.to_csv(f_csv_y_train.format('backward'), index=False)
    x_test_backward.to_csv(f_csv_x_test.format('backward'), index=False)
    y_test_backward.to_csv(f_csv_y_test.format('backward'), index=False)


def create_train_test_domain(domain):
    df = pd.read_csv(csv_fe_dummies)
    cols_features = list(df.columns)
    cols_features.remove('forward')
    cols_features.remove('bi')
    cols_features.remove('backward')
    df_train = df.loc[df[f'domain_{domain}'] == 0]
    df_test = df.loc[df[f'domain_{domain}'] == 1]
    df_train_forward = df_train.drop(['bi', 'backward'], axis=1)
    x_train_forward, y_train_forward = u_df.split_to_x_y(df_train_forward,
                                                         cols_features,
                                                         col_label='forward')
    df_test_forward = df_test.drop(['bi', 'backward'], axis=1)
    x_test_forward, y_test_forward = u_df.split_to_x_y(df_test_forward,
                                                       cols_features,
                                                       col_label='forward')
    df_train_bi = df_train.drop(['forward', 'backward'], axis=1)
    x_train_bi, y_train_bi = u_df.split_to_x_y(df_train_bi,
                                               cols_features,
                                               col_label='bi')
    df_test_bi = df_test.drop(['forward', 'backward'], axis=1)
    x_test_bi, y_test_bi = u_df.split_to_x_y(df_test_bi,
                                             cols_features,
                                             col_label='bi')
    df_train_backward = df_train.drop(['forward', 'bi'], axis=1)
    x_train_backward, y_train_backward = u_df.split_to_x_y(df_train_backward,
                                                           cols_features,
                                                           col_label='backward')
    df_test_backward = df_test.drop(['forward', 'bi'], axis=1)
    x_test_backward, y_test_backward = u_df.split_to_x_y(df_test_backward,
                                                         cols_features,
                                                         col_label='backward')
    dir_domain = dir_storage + '\\by domain\\' + domain
    f_domain_csv_x_train = dir_domain + '\\x_train_{0}.csv'
    f_domain_csv_x_test = dir_domain + '\\x_test_{0}.csv'
    f_domain_csv_y_train = dir_domain + '\\y_train_{0}.csv'
    f_domain_csv_y_test = dir_domain + '\\y_test_{0}.csv'
    x_train_forward.to_csv(f_domain_csv_x_train.format('forward'), index=False)
    y_train_forward.to_csv(f_domain_csv_y_train.format('forward'), index=False)
    x_test_forward.to_csv(f_domain_csv_x_test.format('forward'), index=False)
    y_test_forward.to_csv(f_domain_csv_y_test.format('forward'), index=False)
    x_train_bi.to_csv(f_domain_csv_x_train.format('bi'), index=False)
    y_train_bi.to_csv(f_domain_csv_y_train.format('bi'), index=False)
    x_test_bi.to_csv(f_domain_csv_x_test.format('bi'), index=False)
    y_test_bi.to_csv(f_domain_csv_y_test.format('bi'), index=False)
    x_train_backward.to_csv(f_domain_csv_x_train.format('backward'),
                            index=False)
    y_train_backward.to_csv(f_domain_csv_y_train.format('backward'),
                            index=False)
    x_test_backward.to_csv(f_domain_csv_x_test.format('backward'), index=False)
    y_test_backward.to_csv(f_domain_csv_y_test.format('backward'), index=False)


def create_train_test_map():
    df = pd.read_csv(csv_fe_dummies)
    cols_features = list(df.columns)
    cols_features.remove('forward')
    cols_features.remove('bi')
    cols_features.remove('backward')
    cols_features.remove('map')
    df_train = df.loc[~df['map'].isin(maps_train)]
    df_test = df.loc[df['map'].isin(maps_train)]
    df_train_forward = df_train.drop(['bi', 'backward'], axis=1)
    x_train_forward, y_train_forward = u_df.split_to_x_y(df_train_forward,
                                                         cols_features,
                                                         col_label='forward')
    df_test_forward = df_test.drop(['bi', 'backward'], axis=1)
    x_test_forward, y_test_forward = u_df.split_to_x_y(df_test_forward,
                                                       cols_features,
                                                       col_label='forward')
    df_train_bi = df_train.drop(['forward', 'backward'], axis=1)
    x_train_bi, y_train_bi = u_df.split_to_x_y(df_train_bi,
                                               cols_features,
                                               col_label='bi')
    df_test_bi = df_test.drop(['forward', 'backward'], axis=1)
    x_test_bi, y_test_bi = u_df.split_to_x_y(df_test_bi,
                                             cols_features,
                                             col_label='bi')
    df_train_backward = df_train.drop(['forward', 'bi'], axis=1)
    x_train_backward, y_train_backward = u_df.split_to_x_y(df_train_backward,
                                                           cols_features,
                                                           col_label='backward')
    df_test_backward = df_test.drop(['forward', 'bi'], axis=1)
    x_test_backward, y_test_backward = u_df.split_to_x_y(df_test_backward,
                                                         cols_features,
                                                         col_label='backward')
    dir_domain = dir_storage + '\\by map'
    f_domain_csv_x_train = dir_domain + '\\x_train_{0}.csv'
    f_domain_csv_x_test = dir_domain + '\\x_test_{0}.csv'
    f_domain_csv_y_train = dir_domain + '\\y_train_{0}.csv'
    f_domain_csv_y_test = dir_domain + '\\y_test_{0}.csv'
    x_train_forward.to_csv(f_domain_csv_x_train.format('forward'), index=False)
    y_train_forward.to_csv(f_domain_csv_y_train.format('forward'), index=False)
    x_test_forward.to_csv(f_domain_csv_x_test.format('forward'), index=False)
    y_test_forward.to_csv(f_domain_csv_y_test.format('forward'), index=False)
    x_train_bi.to_csv(f_domain_csv_x_train.format('bi'), index=False)
    y_train_bi.to_csv(f_domain_csv_y_train.format('bi'), index=False)
    x_test_bi.to_csv(f_domain_csv_x_test.format('bi'), index=False)
    y_test_bi.to_csv(f_domain_csv_y_test.format('bi'), index=False)
    x_train_backward.to_csv(f_domain_csv_x_train.format('backward'),
                            index=False)
    y_train_backward.to_csv(f_domain_csv_y_train.format('backward'),
                            index=False)
    x_test_backward.to_csv(f_domain_csv_x_test.format('backward'), index=False)
    y_test_backward.to_csv(f_domain_csv_y_test.format('backward'), index=False)


def create_model(algo):
    x_train = pd.read_csv(f_csv_x_train.format(algo))
    # x_train = x_train.loc[:, ~x_train.columns.str.startswith('map_')]
    # x_train = x_train.loc[:, ~x_train.columns.str.startswith('domain_')]
    y_train = pd.read_csv(f_csv_y_train.format(algo))
    model = u_rfr.create_model(x_train, y_train, verbose=2)
    u_pickle.dump(model, f_pickle_model.format(algo))


def create_model_domain(domain, algo):
    dir_domain = dir_storage + '\\by domain\\' + domain
    f_domain_csv_x_train = dir_domain + '\\x_train_{0}.csv'
    f_domain_csv_y_train = dir_domain + '\\y_train_{0}.csv'
    f_pickle_domain_model = dir_domain + '\\model_{0}.csv'
    x_train = pd.read_csv(f_domain_csv_x_train.format(algo))
    x_train = x_train.loc[:, ~x_train.columns.str.startswith('map_')]
    x_train = x_train.loc[:, ~x_train.columns.str.startswith('domain_')]
    y_train = pd.read_csv(f_domain_csv_y_train.format(algo))
    model = u_rfr.create_model(x_train, y_train, verbose=2)
    u_pickle.dump(model, f_pickle_domain_model.format(algo))


def create_model_map(algo):
    dir_domain = dir_storage + '\\by map'
    f_domain_csv_x_train = dir_domain + '\\x_train_{0}.csv'
    f_domain_csv_y_train = dir_domain + '\\y_train_{0}.csv'
    f_pickle_domain_model = dir_domain + '\\model_{0}.csv'
    x_train = pd.read_csv(f_domain_csv_x_train.format(algo))
    y_train = pd.read_csv(f_domain_csv_y_train.format(algo))
    model = u_rfr.create_model(x_train, y_train, verbose=2)
    u_pickle.dump(model, f_pickle_domain_model.format(algo))


def predict(algo):
    model = u_pickle.load(f_pickle_model.format(algo))
    x_test = pd.read_csv(f_csv_x_test.format(algo))
    # x_test = x_test.loc[:, ~x_test.columns.str.startswith('map_')]
    # x_test = x_test.loc[:, ~x_test.columns.str.startswith('domain_')]
    y_test = pd.read_csv(f_csv_y_test.format(algo))
    y_pred = u_rfr.predict(model, x_test)
    y_pred = pd.DataFrame(y_pred)
    y_pred.columns = ['pred']
    y_test['pred'] = y_pred['pred']
    y_test.to_csv(f_csv_pred.format(algo))


def predict_domain(domain, algo):
    dir_domain = dir_storage + '\\by domain\\' + domain
    f_domain_csv_x_test = dir_domain + '\\x_test_{0}.csv'
    f_domain_csv_y_test = dir_domain + '\\y_test_{0}.csv'
    f_pickle_domain_model = dir_domain + '\\model_{0}.csv'
    f_domain_csv_pred = dir_domain + '\\pred_{0}.csv'
    model = u_pickle.load(f_pickle_domain_model.format(algo))
    x_test = pd.read_csv(f_domain_csv_x_test.format(algo))
    x_test = x_test.loc[:, ~x_test.columns.str.startswith('map_')]
    x_test = x_test.loc[:, ~x_test.columns.str.startswith('domain_')]
    y_test = pd.read_csv(f_domain_csv_y_test.format(algo))
    y_pred = u_rfr.predict(model, x_test)
    y_pred = pd.DataFrame(y_pred)
    y_pred.columns = ['pred']
    y_test['pred'] = y_pred['pred']
    y_test.to_csv(f_domain_csv_pred.format(algo))


def predict_map():
    dir_domain = dir_storage + '\\by map'
    f_domain_csv_x_test = dir_domain + '\\x_test_{0}.csv'
    f_domain_csv_y_test = dir_domain + '\\y_test_{0}.csv'
    f_pickle_domain_model = dir_domain + '\\model_{0}.csv'
    f_domain_csv_pred = dir_domain + '\\pred_{0}.csv'
    for algo in {'forward', 'bi', 'backward'}:
        model = u_pickle.load(f_pickle_domain_model.format(algo))
        x_test = pd.read_csv(f_domain_csv_x_test.format(algo))
        y_test = pd.read_csv(f_domain_csv_y_test.format(algo))
        y_pred = u_rfr.predict(model, x_test)
        y_pred = pd.DataFrame(y_pred)
        y_pred.columns = ['pred']
        y_test['pred'] = y_pred['pred']
        y_test.to_csv(f_domain_csv_pred.format(algo))


def predict_bestgrid(algo):
    model = u_pickle.load(f_pickle_model.format(f'{algo}_bestgrid'))
    x_test = pd.read_csv(f_csv_x_test.format(algo))
    # x_test = x_test.loc[:, ~x_test.columns.str.startswith('map_')]
    # x_test = x_test.loc[:, ~x_test.columns.str.startswith('domain_')]
    y_test = pd.read_csv(f_csv_y_test.format(algo))
    y_pred = u_rfr.predict(model, x_test)
    y_pred = pd.DataFrame(y_pred)
    y_pred.columns = ['pred']
    y_test['pred'] = y_pred['pred']
    y_test.to_csv(f_csv_pred.format(f'{algo}_bestgrid'))


def join_pred():
    pred_forward = pd.read_csv(f_csv_pred.format('forward'))
    pred_bi = pd.read_csv(f_csv_pred.format('bi'))
    pred_backward = pd.read_csv(f_csv_pred.format('backward'))
    df_all = pred_forward.rename(columns={'label': 'forward',
                                          'pred': 'pred_forward'})
    df_all['bi'] = pred_bi['label']
    df_all['pred_bi'] = pred_bi['pred']
    df_all['backward'] = pred_backward['label']
    df_all['pred_backward'] = pred_backward['pred']
    df_all.to_csv(f_csv_pred.format('all'))


def join_pred_domain(domain):
    dir_domain = dir_storage + '\\by domain\\' + domain
    f_domain_csv_pred = dir_domain + '\\pred_{0}.csv'
    pred_forward = pd.read_csv(f_domain_csv_pred.format('forward'))
    pred_bi = pd.read_csv(f_domain_csv_pred.format('bi'))
    pred_backward = pd.read_csv(f_domain_csv_pred.format('backward'))
    df_all = pred_forward.rename(columns={'label': 'forward',
                                          'pred': 'pred_forward'})
    df_all['bi'] = pred_bi['label']
    df_all['pred_bi'] = pred_bi['pred']
    df_all['backward'] = pred_backward['label']
    df_all['pred_backward'] = pred_backward['pred']
    df_all.to_csv(f_domain_csv_pred.format('all'))


def join_pred_map():
    dir_domain = dir_storage + '\\by map'
    f_domain_csv_pred = dir_domain + '\\pred_{0}.csv'
    pred_forward = pd.read_csv(f_domain_csv_pred.format('forward'))
    pred_bi = pd.read_csv(f_domain_csv_pred.format('bi'))
    pred_backward = pd.read_csv(f_domain_csv_pred.format('backward'))
    df_all = pred_forward.rename(columns={'label': 'forward',
                                          'pred': 'pred_forward'})
    df_all['bi'] = pred_bi['label']
    df_all['pred_bi'] = pred_bi['pred']
    df_all['backward'] = pred_backward['label']
    df_all['pred_backward'] = pred_backward['pred']
    df_all.to_csv(f_domain_csv_pred.format('all'))


def grid_search(algo):
    model = u_pickle.load(f_pickle_model.format(algo))
    x_train = pd.read_csv(f_csv_x_train.format(algo))
    y_train = pd.read_csv(f_csv_y_train.format(algo))
    n_estimators = [100, 300, 500, 800, 1200]
    max_depth = [5, 8, 15, 25, 30]
    min_samples_split = [2, 5, 10, 15, 100]
    min_samples_leaf = [1, 2, 5, 10]

    hyperF = dict(n_estimators=n_estimators, max_depth=max_depth,
                  min_samples_split=min_samples_split,
                  min_samples_leaf=min_samples_leaf)

    gridF = GridSearchCV(model, hyperF, cv=3, verbose=1, n_jobs=-1)
    bestF = gridF.fit(x_train, y_train)
    u_pickle.dump(bestF, f_pickle_model.format(f'{algo}_bestgrid'))

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
#union_results()
# best_results()
# create_fe_raw('mazes')
# create_fe_raw('random')
# create_fe_raw('rooms')
# create_fe_raw('games')
# create_fe_raw('cities')
# union_fe_raw()
# join_results_fe_raw()
# create_fe_dummies()
# create_train_test()
# create_train_test_domain('cities')
# create_train_test_domain('games')
# create_train_test_domain('mazes')
# create_train_test_domain('random')
# create_train_test_domain('rooms')
# create_model('forward')
# create_model('bi')
# create_model('backward')
# for domain in {'cities', 'games', 'mazes', 'random', 'rooms'}:
#    for algo in {'forward', 'bi', 'backward'}:
#        create_model_domain(domain, algo)
# predict('forward')
# predict('bi')
# predict('backward')
# for domain in {'cities', 'games', 'mazes', 'random', 'rooms'}:
#     for algo in {'forward', 'bi', 'backward'}:
#         predict_domain(domain, algo)
# join_pred()
# for domain in {'cities', 'games', 'mazes', 'random', 'rooms'}:
#    join_pred_domain(domain)
# create_forward_mazes()
# create_regret('cities')
# create_regret('games')
# create_regret('mazes')
# create_regret('random')
# create_regret('rooms')
# create_fe_dummies_map()
# create_train_test_map()
# for algo in {'forward', 'bi', 'backward'}:
#    create_model_map(algo)
# predict_map()
# join_pred_map()
# grid_search('forward')
# grid_search('bi')
# grid_search('backward')
# predict_bestgrid('forward')
# predict_bestgrid('bi')
# predict_bestgrid('backward')
#create_optimal('cities')
create_optimal('games')
#create_optimal('mazes')
#create_optimal('random')
#create_optimal('rooms')
