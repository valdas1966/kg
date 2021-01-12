from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.astar_lookup_early import AStarLookupEarly
from f_utils import u_pickle
from f_excel.c_excel_map import ExcelMap
from f_utils import u_file


dir_storage = 'D:\\Exp\\'
pickle_grids = dir_storage + 'grids.pickle'
pickle_results = dir_storage + 'results_early.pickle'
csv_report_early = dir_storage + 'report_early.csv'
xls_template = dir_storage + 'template_draw.xlsx'
xls_draw = dir_storage + 'draw.xlsx'


def create_results():
    results = list()
    while len(results) < 1000:
        grid = GridBlocks(rows=10, percent_blocks=30)
        start, goal_1, goal_2 = grid.points_random(amount=3)
        astar_forward = AStarLookupEarly(grid, start, goal_1)
        astar_forward.run()
        if not astar_forward.is_found:
            continue
        lookup = astar_forward.lookup_start()
        astar_backward = AStarLookupEarly(grid, goal_2, start, lookup)
        astar_backward.run()
        if not astar_backward.is_found:
            continue
        astar_true = AStarLookupEarly(grid, start, goal_2)
        astar_true.run()
        results.append((astar_forward, astar_backward, astar_true))
        print(len(results))
    u_pickle.dump(results, pickle_results)


def create_report():
    results = u_pickle.load(pickle_results)
    file = open(csv_report_early, 'w')
    file.write('i, f_lookup, f_early\n')
    for i, (astar_forward, astar_backward, astar_true) in enumerate(results):
        f_lookup = astar_backward.f_value()
        f_true = astar_true.f_value()
        file.write(f'{i}, {f_lookup}, {f_true}\n')
    file.close()


# create_results()
# create_report()

u_file.delete(xls_draw)
u_file.copy(xls_template, xls_draw)

results = u_pickle.load(pickle_results)
astar_forward, astar_backward, astar_true = results[6]
grid = astar_forward.grid
xl_map = ExcelMap(xlsx=xls_draw)
grid.draw_excel(xl_map, row_start=2, col_start=2, title='Map',
                with_numbers=True)
xl_map.close()
