from experiments.pathmax import u_features
from model.point import Point
from model.grid import Grid


p_1 = Point(0, 0, 'a')
p_2 = Point(1, 1, 'b')
p_3 = Point(2, 2, 'c')
points = [p_1, p_2, p_3]

distances = u_features.distances(points)
for k, v in distances.items():
    print(k, v)

print()

grid = Grid(rows=5)
from_center = u_features.from_center(grid, points)
for p in from_center:
    print(p, from_center[p])