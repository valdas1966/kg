import random
from f_utils import u_pickle
from proj.ai.model.point import Point
from proj.ai.model.grid_blocks import GridBlocks
from proj.ai.algo.astar import AStar

pickle_grids = 'D:\\Exp_RooMap\\grids.pickle'
csv_random = 'D:\\Exp\\Symmetry_Random_512x512.csv'
csv_roomap = 'D:\\Exp\\Symmetry_RooMap.csv'


def run_random():
    """
    ============================================================================
     Description: Run 1000 experiments on random 10x10 maps to check symmetry
                    on A* search on maps with obstacles.
    ============================================================================
    """
    results = list()
    while len(results) < 1000:
        grid = GridBlocks(rows=512, percent_blocks=30)
        start, goal = grid.points_random(amount=2)
        forward, backward = run_symmetry(grid, start, goal)
        if forward:
            results.append((forward, backward))
        print(len(results))
    file = open(csv_random, 'w')
    file.write(f'forward,backward\n')
    for forward, backward in results:
        file.write(f'{forward},{backward}\n')
    file.close()


def run_rooms():
    results = list()
    grids = u_pickle.load(pickle_grids)
    for i in range(1000):
        j = random.randint(0, len(grids)-1)
        grid = grids[j]
        start, goal = grid.points_random(amount=2)
        astar_forward = AStar(grid, start, goal)
        astar_forward.run()
        forward = astar_forward.expanded_nodes()
        astar_backward = AStar(grid, goal, start)
        astar_backward.run()
        backward = astar_backward.expanded_nodes()
        results.append((forward, backward))
        print(i)
    file = open(csv_roomap, 'w')
    file.write('forward,backward\n')
    for forward, backward in results:
        file.write(f'{forward},{backward}\n')
    file.close()


def run_symmetry(grid, start, goal):
    """
    ============================================================================
     Description: Run A* in both directions and return the amount of
                    expanded nodes.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : GridBlocks
        2. start : Point
        3. goal : Point
    ============================================================================
     Return: Tuple(int [forward expanded nodes], int [backward expanded nodes])
    ============================================================================
    """
    assert type(grid) == GridBlocks
    assert type(start) == Point
    assert type(goal) == Point
    astar_forward = AStar(grid, start, goal)
    astar_forward.run()
    if not astar_forward.is_found:
        return 0, 0
    forward = astar_forward.expanded_nodes()
    astar_backward = AStar(grid, goal, start)
    astar_backward.run()
    backward = astar_backward.expanded_nodes()
    return forward, backward


# run_random()
run_rooms()
