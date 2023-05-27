from f_utils import u_pickle
from f_utils import u_file
from logic import u_grid_blocks
from f_db.c_sqlite import SQLite
import pandas as pd
import config


path_grids = config.path_grids
csv_pairs = config.path_pairs + '\\pairs.csv'
csv_stat = config.path_pairs + '\\stat.csv'

f = open(csv_pairs, 'w')
f.write('domain,map,distance,x1,y1,x2,y2\n')
pickles = u_file.filepaths(path_dir=path_grids)
for p in pickles:
    grid = u_pickle.load(path=p)
    domain = p.split('_')[0].split('\\')[-1]
    map = p.split('_')[1].split('.')[0]
    pairs = u_grid_blocks.random_pairs_by_distance(grid=grid,
                                                   amount=1000,
                                                   size=100)
    for distance, li in pairs.items():
        for p1, p2 in li:
            print(domain, map, distance, p1.x, p1.y, p2.x, p2.y)
            f.write(f'{domain},{map},{distance},{p1.x},{p1.y},{p2.x},{p2.y}\n')
f.close()

df = pd.read_csv(csv_pairs)

sql = SQLite()

sql.load(tname='temp_1', df=df)

query = """
            select
                domain,
                map,
                distance, 
                count(*) as cnt
            from
                temp_1
            group by
                domain,
                map,
                distance
        """

sql.select(query=query).to_csv(csv_stat)
