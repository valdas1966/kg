from model.grid_blocks import GridBlocks
from model.kspp import KSPP


grid = GridBlocks(rows=3, percent_blocks=0)
kspps = KSPP.generate_random(grid=grid, n=5, k=2, radius=1)

print(kspps)
