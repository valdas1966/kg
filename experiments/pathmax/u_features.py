from collections import defaultdict
from itertools import combinations
from model.point import Point
from model.grid import Grid
from logic import u_grid


def distances(nodes: dict) -> dict:
    res = dict()
    for a, b in combinations(nodes, 2):
        name = f'dist_{a}_{b}'
        dist = nodes[a].distance(nodes[b])
        res[name] = dist
    return res


def from_center(grid: Grid, nodes: dict) -> dict:
    res = dict()
    for node in nodes.values():
        name = f'dist_center_{node.name}'
        res[name] = u_grid.distance_from_center(grid, node)
    return res


def closed(astars: dict) -> dict:
    res = dict()
    for astar in astars.values():
        name = f'closed_{astar.name}'
        res[name] = len(astar.closed)
    return res


def optimal(astars: dict) -> dict:
    res = dict()
    for astar in astars.values():
        name = f'optimal_{astar.name}'
        res[name] = len(astar.optimal_path())
    return res


def inter(astars: dict) -> dict:
    res = dict()
    vals = astars.values()
    for a, b in combinations(vals, 2):
        name = f'inter_{a.name}_{b.name}'
        res[name] = len(a.closed.intersection(b.closed))
    return res
