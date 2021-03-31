from collections import defaultdict
import datetime
from algo.astar import AStar
from algo.kastar_projection import KAStarProjection
from algo.kastar_bi import KAStarBi
from algo.kastar_backward import KAStarBackward
from logic import u_grid_blocks
from f_utils import u_file
from f_utils import u_pickle
import pandas as pd


dir_maps = 'd:\\temp\\maps\\'
dir_storage = 'd:\\temp\\final\\'
dir_storage = 'g:\\roni\\model\\'
dir_forward = dir_storage + 'Forward\\'
pickle_grids = dir_storage + 'grids.pickle'
pickle_grids_final = dir_storage + 'grids_final.pickle'
pickle_pairs = dir_storage + 'pairs.pickle'
f_pickle_pairs = dir_storage + 'pairs_{0}.pickle'
f_pickle_sg = dir_storage + 'sg_{0}.pickle'
f_pickle_forward = dir_forward + '{0}_{1}_{2}_{3}_{4}.pickle'
csv_grids = dir_storage + 'grids.csv'
csv_sg_pairs = dir_storage + 'sg_pairs.csv'
csv_sg = dir_storage + 'sg.csv'
f_csv_found = dir_storage + 'found_{0}.csv'
f_csv_forward = dir_storage + 'forward_{0}.csv'
f_csv_bi = dir_storage + 'bi_{0}.csv'


def create_grids():
    d_grids = defaultdict(dict)
    for filepath in u_file.filepaths(dir_maps):
        domain = filepath.split('\\')[-2]
        if domain not in d_grids:
            d_grids[domain] = defaultdict(dict)
        map = filepath.split('\\')[-1].replace('.map','')
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


def create_sg_pairs():
    d_sg_pairs = dict()
    d_grids = u_pickle.load(pickle_grids_final)
    for domain in d_grids:
        d_sg_pairs[domain] = dict()
        for map, grid in d_grids[domain].items():
            pairs = u_grid_blocks.random_pairs_by_distance(grid,
                                                           amount=10000000,
                                                           size=100)
            d_sg_pairs[domain][map] = pairs
            print(domain, map)
    u_pickle.dump(d_sg_pairs, pickle_pairs)


def print_sg_pairs():
    d_sg_pairs = u_pickle.load(pickle_pairs)
    file = open(csv_sg_pairs, 'w')
    file.write('domain,map,distance,pairs\n')
    for domain in sorted(d_sg_pairs):
        for map in sorted(d_sg_pairs[domain]):
            for distance in sorted(d_sg_pairs[domain][map]):
                pairs = d_sg_pairs[domain][map][distance]
                file.write(f'{domain},{map},{distance},{len(pairs)}\n')
    file.close()


def split_pairs():
    d_pairs = u_pickle.load(pickle_pairs)
    u_pickle.dump(d_pairs['cities'], pickle_pairs_cities)
    u_pickle.dump(d_pairs['games'], pickle_pairs_games)
    u_pickle.dump(d_pairs['mazes'], pickle_pairs_mazes)
    u_pickle.dump(d_pairs['random'], pickle_pairs_random)
    u_pickle.dump(d_pairs['rooms'], pickle_pairs_rooms)


def create_sg(domain, pickle_pairs_domain, pickle_sg):
    d_grids = u_pickle.load(pickle_grids)
    d_pairs_domain = u_pickle.load(pickle_pairs_domain)
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
    u_pickle.dump(d_sg, pickle_sg)


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
        if map == 'maze512-1-0':
            continue
        grid = d_grids[domain][map]
        for k in sorted(d_sg[domain][map]):
            for distance in sorted(d_sg[domain][map][k]):
                li_sg = d_sg[domain][map][k][distance]
                for i, (start, goals) in enumerate(li_sg):
                    kastar = KAStarProjection(grid, start, goals)
                    kastar.run()
                    pickle = f_pickle_forward.format(domain, map, k,
                                                     distance, i)
                    u_pickle.dump(kastar, pickle)
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
                    kastar = KAStarBi(grid, start, goals)
                    kastar.run()
                    nodes = sum(kastar.closed.values())
                    if not kastar.is_found:
                        nodes = -1
                    file = open(f_csv_bi.format(domain), 'a')
                    file.write(f'{domain},{map},{k},{distance},{i},{nodes}\n')
                    file.close()
                    print(datetime.datetime.now(), domain, map, k, distance, i)


# create_grids()
# print_grids()
# create_grids_final()
# create_sg_pairs()
# print_sg_pairs()
# split_pairs()
# create_sg('random', pickle_pairs_random, pickle_sg_random)
# print_sg()
# print_found('mazes')
# print_found('random')
# print_found('rooms')
create_forward('mazes')
# create_forward('random')
# create_forward('rooms')
# create_bi('mazes')
# create_bi('random')
# create_bi('rooms')


# mazes maze512-1-0 2 500 9
d_grids = u_pickle.load(pickle_grids_final)
grid = d_grids['mazes']['maze512-1-0']
d_sg = u_pickle.load(f_pickle_sg.format('mazes'))
start, goals = d_sg['mazes']['maze512-1-0'][3][0][0]
print(start, goals)
kastar = KAStarProjection(grid, start, goals)
kastar.run()
print(len(kastar.closed))