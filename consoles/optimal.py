import pandas as pd
from f_db.c_sqlite import SQLite


repo = 'D:\\Temp\\write\\222802\\'
csv_final_union = repo + 'final_union.csv'
csv_optimal_union = repo + 'optimal_union.csv'
csv_union = repo + 'union.csv'
f_csv_optimal = repo + 'optimal_{0}.csv'


def create_optimal_union():
    domains = ['cities', 'games', 'mazes', 'random', 'rooms']
    df_all = pd.DataFrame()
    for domain in domains:
        csv = f_csv_optimal.format(domain)
        df = pd.read_csv(csv)
        df_all = df_all.append(df)
    df_all.to_csv(csv_optimal_union)


def create_final_union():
    df_union = pd.read_csv(csv_union)
    df_optimal = pd.read_csv(csv_optimal_union)
    sql = SQLite()
    sql.load(tname='temp_1', df=df_union, verbose=True)
    sql.load(tname='temp_2', df=df_optimal, verbose=True)
    query = """
                select
                    t1.domain,
                    t1.map,
                    t1.k,
                    t1.distance,
                    t1.i,
                    t1.forward,
                    t1.bi,
                    t1.backward,
                    t1.oracle,
                    t2.optimal,
                    t1.winner
                from
                    temp_1 t1,
                    temp_2 t2
                where
                    t1.domain = t2.domain
                    and
                    t1.map = t2.map
                    and
                    t1.k = t2.k
                    and
                    t1.distance = t2.distance
                    and
                    t1.i = t2.i
            """
    sql.select(query).to_csv(csv_final_union)


# create_optimal_union()
create_final_union()