import pandas as pd
import random
from model.point import Point
from model.problem import Problem
import logic.u_grid_blocks as logic
import config


csv_pairs = f'{config.path_pairs}\\pairs.csv'

df = pd.read_csv(csv_pairs)[:5]

print(df)

print()

problems = list()
for _, row in df.iterrows():
    domain = row['domain']
    map = row['map']
    start = Point(row['x1'], row['y1'])
    radius = 5
    amount = random.randint(2, 10)
    goals = logic.random_points_radius(start, radius=radius, amount=amount)

