from model.grid_blocks import GridBlocks
from algo.kastar_projection import KAStarProjection
from f_utils import u_pickle
from f_db.c_sqlite import SQLite
import random
import pandas as pd

repo = 'd:\\temp\\write\\exp ka projection goal order\\'
pickle_problems = repo + 'problems.pickle'
csv_min = repo + 'min.csv'
csv_max = repo + 'max.csv'
csv_rand = repo + 'random.csv'
csv_output = repo + 'results.csv'
csv_agg = repo + 'agg.csv'


def create_problems():
    problems = list()
    for i in range(100000):
        percent_blocks = random.randint(1, 80)
        grid = GridBlocks(rows=10, percent_blocks=percent_blocks)
        cnt_goals = random.randint(2, 10)
        points = grid.points_random(amount=cnt_goals + 1)
        start = points[0]
        goals = points[1:]
        problems.append((grid, start, goals, percent_blocks))
        if not i % 1000:
            print(i)
    u_pickle.dump(problems, pickle_problems)


def run(csv):
    problems = u_pickle.load(pickle_problems)
    file = open(csv, 'w')
    file.write('i,goals,blocks,nodes\n')
    for i, p in enumerate(problems):
        grid, start, goals, blocks = p
        ka = KAStarProjection(grid, start, goals)
        ka.run()
        if not ka.is_found:
            continue
        file.write(f'{i},{len(goals)},{blocks},{len(ka.closed)}\n')
        if not i % 1000:
            print(i)
    file.close()


def aggregate():
    df_1 = pd.read_csv(csv_output)
    sql = SQLite()
    sql.load(df_1, tname='temp_1')
    query = """
                select
                    goals,
                    round(avg(min),0) as min,
                    round(avg(rand),0) as rand,
                    round(avg(max), 0) as max
                from
                    temp_1
                group by
                    goals
                order by 1
            """
    df_2 = sql.select(query)
    df_2.to_csv(csv_agg)


# create_problems()
# run(csv_rand)
aggregate()