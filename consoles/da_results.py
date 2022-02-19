import pandas as pd
from f_db.c_sqlite import SQLite


repo = 'g:\\temp\\thesis\\results\\'
csv_forward = repo + 'forward.csv'
csv_backward = repo + 'backward.csv'
csv_bi = repo + 'bi.csv'
csv_optimal = repo + 'optimal.csv'
csv_union = repo + 'union.csv'
csv_agg_opt_for = repo + 'agg_opt_for.csv'
csv_agg_opt_for = repo + 'agg_opt_for.csv'
csv_agg_wins = repo + 'agg_wins_domain.csv'
csv_agg_for_back = repo + 'agg_for_back.csv'
csv_agg_for_back_domain = repo + 'agg_for_back_domain.csv'


def union():
    sql = SQLite()
    df_forward = pd.read_csv(csv_forward)
    df_bi = pd.read_csv(csv_bi)
    df_backward = pd.read_csv(csv_backward)
    df_optimal = pd.read_csv(csv_optimal)
    sql.load(tname='forward', df=df_forward, verbose=True)
    sql.load(tname='bi', df=df_bi, verbose=True)
    sql.load(tname='backward', df=df_backward, verbose=True)
    query = """
                select
                    t1.domain,
                    t1.map,
                    t1.k,
                    t1.distance,
                    t1.i,
                    t1.forward,
                    t2.bi,
                    t3.backward
                from
                    forward t1,
                    bi t2,
                    backward t3
                where
                    t1.domain = t2.domain
                    and
                    t2.domain = t3.domain
                    and
                    t1.map = t2.map
                    and
                    t2.map = t3.map
                    and
                    t1.k = t2.k
                    and
                    t2.k = t3.k
                    and
                    t1.distance = t2.distance
                    and
                    t2.distance = t3.distance
                    and
                    t1.i = t2.i
                    and
                    t2.i = t3.i
                    and
                    t1.forward > 0
                    and
                    t2.bi > 0
                    and
                    t3.backward > 0
                order by
                    t1.domain,
                    t1.map,
                    t1.k,
                    t1.distance,
                    t1.i
                """
    sql.ctas(tname='temp_1', query=query, verbose=True)
    query = """
                select
                    t1.*,
                    case
                        when forward<=bi and forward <= backward then forward
                        when bi<=forward and bi<=backward then bi
                        when backward<=bi and backward<=forward then backward
                        end as oracle,
                    case
                        when bi<=forward and bi<=backward then 'Bi'
                        when backward<=forward then 'Backward'
                        else 'Forward' end as winner
                from
                    temp_1 t1
            """
    sql.ctas(tname='temp_2', query=query)
    sql.load(tname='optimal', df=df_optimal, verbose=True)
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
                    t1.winner,
                    t2.optimal
                from
                    temp_2 t1
                left join
                    optimal t2
                on
                    t1.domain = t2.domain
                    and
                    t1.map = t2.map
                    and
                    t1.k = t2.k
                    and
                    t1.distance = t2.distance
                    and
                    t1.i = t2.i
                order by
                    t1.domain,
                    t1.map,
                    t1.k,
                    t1.distance,
                    t1.i
            """
    df_union = sql.select(query=query, verbose=True)
    df_union.to_csv(csv_union)


def agg_opt_for():
    df_union = pd.read_csv(csv_union)
    sql = SQLite()
    sql.load(tname='temp', df=df_union)
    query = """
                select
                    domain,
                    round(avg(cast(optimal as float)/forward),2) as opt_for
                from
                    temp
                where
                    optimal is not null
                group by
                    domain
                order by 1
            """
    sql.select(query=query).to_csv(csv_agg_opt_for)


def agg_wins():
    df_union = pd.read_csv(csv_union)
    sql = SQLite()
    sql.load(tname='temp', df=df_union)
    query = """
                select
                    winner,
                    count(*) as cnt
                from
                    temp
                group by
                    winner
                order by 1, 2
            """
    sql.select(query=query).to_csv(csv_agg_wins)


def agg_optimal_equal():
    df_union = pd.read_csv(csv_union)
    sql = SQLite()
    sql.load(tname='temp', df=df_union)
    query = """
                    select
                        count(*) as cnt,
                        sum(case when optimal=forward then 1 else 0 end) as eq
                    from
                        temp
                """
    print(sql.select(query=query))


def agg_for_back():
    df_union = pd.read_csv(csv_union)
    sql = SQLite()
    sql.load(tname='temp_1', df=df_union)
    query = """
                select
                    winner,
                    count(*) as cnt
                from
                    (
                        select
                            case
                                when backward < forward then 'Backward'
                                when backward = forward then 'Equal'
                                else 'Forward' end as winner
                            from
                                temp_1
                    ) t1
                group by
                    winner
                order by 1
            """



union()
#agg_opt_for()
#agg_wins()
#agg_optimal_equal()