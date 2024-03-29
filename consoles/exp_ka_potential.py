from model.grid_blocks import GridBlocks
from algo.kastar_projection import KAStarProjection
from f_utils import u_pickle
from f_db.c_sqlite import SQLite
import random
import pandas as pd

repo = 'g:\\temp\\thesis\\exp ka potential\\'
repo = 'd:\\temp\\write\\exp ka potential\\'
pickle_problems = repo + 'problems.pickle'
csv_results = repo + 'results.csv'
csv_agg = repo + 'agg.csv'


def create_problems():
    problems = list()
    i = 0
    while i < 100000:
        grid = GridBlocks(rows=10, percent_blocks=20)
        cnt_goals = random.randint(2, 10)
        points = grid.points_random(amount=cnt_goals + 1)
        start = points[0]
        goals = points[1:]
        ka = KAStarProjection(grid, start, goals)
        ka.run()
        if not ka.is_found:
            continue
        problems.append((grid, start, goals))
        if not i % 1000:
            print(i)
        i += 1
    u_pickle.dump(problems, pickle_problems)


def run():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_results, 'w')
    file.write('i,goals,closed,optimal\n')
    for i, p in enumerate(problems):
        grid, start, goals = p
        ka = KAStarProjection(grid, start, goals)
        ka.run()
        if not ka.is_found:
            continue
        file.write(f'{i},{len(goals)},{len(ka.closed)},'
                   f'{len(ka.optimal_nodes)}\n')
        if not i % 1000:
            print(i)
    file.close()


def aggregate():
        df = pd.read_csv(csv_results)
        sql = SQLite()
        sql.load(df, tname='temp')
        query = """
                    select
                        goals,
                        round(avg(closed),0) as closed,
                        round(avg(optimal),0) as optimal
                    from
                        temp
                    group by
                        goals
                    order by 1
                """
        sql.select(query, verbose=True).to_csv(csv_agg)


# create_problems()
run()
# aggregate()
