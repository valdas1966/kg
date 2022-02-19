from model.grid_blocks import GridBlocks
from algo.kastar_projection import KAStarProjection
from algo.kastar_bi import KAStarBi
from algo.kastar_backward import KAStarBackward
from f_utils import u_pickle
from f_db.c_sqlite import SQLite
import random
import pandas as pd


#repo = 'd:\\temp\\write\\exp ka directions\\'
repo = 'g:\\temp\\thesis\\exp ka directions\\'
#repo = 'g:\\temp\\thesis\\exp ka directions 50 goals\\'
pickle_problems = repo + 'problems.pickle'
csv_results = repo + 'results.csv'
csv_opt_for = repo + 'opt_for.csv'
csv_wins = repo + 'wins.csv'
csv_expanded_nodes = repo + 'expanded_nodes.csv'


def create_problems():
    problems = list()
    i = 0
    while i < 500000:
        grid = GridBlocks(rows=10, percent_blocks=20)
        cnt_goals = random.randint(2, 50)
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
    file.write('i,goals,forward,bi,backward,oracle,optimal,winner\n')
    for i, p in enumerate(problems):
        grid, start, goals = p
        ka_forward = KAStarProjection(grid, start, goals)
        ka_forward.run()
        forward = len(ka_forward.closed)
        optimal_nodes = set()
        for li in ka_forward.optimal_paths.values():
            optimal_nodes.update(set(li))
        optimal = len(optimal_nodes)
        ka_bi = KAStarBi(grid, start, goals)
        ka_bi.run()
        bi = ka_bi.expanded_nodes()
        ka_backward = KAStarBackward(grid, start, goals)
        ka_backward.run()
        backward = ka_backward.expanded_nodes()
        oracle = min(forward, bi, backward)
        winner = 'Forward'
        if oracle == backward:
            winner = 'Backward'
        elif oracle == bi:
            winner = 'Bi'
        file.write(f'{i},{len(goals)},{forward},{bi},{backward},{oracle},'
                   f'{optimal},{winner}\n')
        if not i % 1000:
            print(i)
    file.close()


def agg_opt_for():
    df_results = pd.read_csv(csv_results)
    sql = SQLite()
    sql.load(df=df_results, tname='results')
    query = """
                select
                    goals,
                    round(avg(cast(optimal as float)/forward),2) as opt_for
                from
                    results
                group by 
                    goals
                order by 1
            """
    df_opt_for = sql.select(query)
    df_opt_for.to_csv(csv_opt_for)


def agg_wins():
    df_results = pd.read_csv(csv_results)
    sql = SQLite()
    sql.load(df=df_results, tname='results')
    query = """
                    select
                        winner,
                        count(*) as cnt
                    from
                        results
                    group by 
                        winner
                    order by 1
                """
    df_opt_for = sql.select(query)
    df_opt_for.to_csv(csv_wins)


def agg_expanded_nodes():
    df_results = pd.read_csv(csv_results)
    sql = SQLite()
    sql.load(df=df_results, tname='results')
    query = """
                    select
                        goals,
                        round(avg(forward),0) as forward,
                        round(avg(bi),0) as bi,
                        round(avg(backward),0) as backward,
                        round(avg(oracle),0) as oracle,
                        round(avg(optimal),0) as optimal
                    from
                        results
                    group by 
                        goals
                    order by 1
                """
    df_opt_for = sql.select(query)
    df_opt_for.to_csv(csv_expanded_nodes)

# create_problems()
# run()
# agg_opt_for()
# agg_wins()
agg_expanded_nodes()
