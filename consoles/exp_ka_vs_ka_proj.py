from model.grid_blocks import GridBlocks
from algo.kastar_eager import KAStarEager
from algo.kastar_projection import KAStarProjection
from f_utils import u_pickle
from f_db.c_sqlite import SQLite
import random
import pandas as pd

repo = 'd:\\temp\\write\\exp ka ka projection\\'
pickle_problems = repo + 'problems.pickle'
csv_results = repo + 'results.csv'
csv_agg_nodes = repo + 'agg_nodes.csv'
csv_agg_wins = repo + 'agg_wins.csv'
csv_agg_h = repo + 'agg_h.csv'


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


def run():
    problems = u_pickle.load(pickle_problems)
    file = open(csv_results, 'w')
    file.write('i,goals,blocks,ka_nodes,ka_h,proj_nodes,proj_h\n')
    for i, p in enumerate(problems):
        grid, start, goals, blocks = p
        proj = KAStarProjection(grid, start, goals)
        proj.run()
        if not proj.is_found:
            continue
        ka = KAStarEager(grid, start, goals)
        ka.run()
        file.write(f'{i},{len(goals)},{blocks},{len(ka.closed)},'
                   f'{ka.comp_h},{len(proj.closed)},'
                   f'{len(proj.closed)+len(proj.opened._opened)}\n')
        if not i % 1000:
            print(i)
    file.close()


def aggregate_nodes():
    df_1 = pd.read_csv(csv_results)
    sql = SQLite()
    sql.load(df_1, tname='temp_0')
    query = """
                select
                    goals,
                    round(avg(ka_nodes),2) as ka,
                    round(avg(proj_nodes),2) as proj
                from
                    temp_0
                group by
                    goals
                order by 1
            """
    sql.select(query).to_csv(csv_agg_nodes)
    query = """
                select
                    sum(case when ka_nodes<proj_nodes then 1 else 0 end) as ka,
                    sum(case when ka_nodes=proj_nodes then 1 else 0 end) as 
                    equal,
                    sum(case when ka_nodes>proj_nodes then 1 else 0 end) as 
                    proj
                from
                    temp_0
            """
    sql.select(query).to_csv(csv_agg_wins)


def aggregate_h():
    df_1 = pd.read_csv(csv_results)
    sql = SQLite()
    sql.load(df_1, tname='temp_0')
    query = """
                select
                    goals,
                    round(avg(ka_h),0) as ka,
                    round(avg(proj_h),0) as proj
                from
                    temp_0
                group by
                    goals
                order by 1
            """
    sql.select(query).to_csv(csv_agg_h)



# create_problems()
# run()
# aggregate_nodes()
aggregate_h()