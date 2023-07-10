from model.grid_blocks import GridBlocks
from model.kspp import KSPP


def test_generate_random() -> None:
    grid = GridBlocks(rows=3, percent_blocks=0)
    kspss = KSPP.generate_random(grid=grid,
                                 n_kspp=5,
                                 n_goals=2,
                                 radius=1)
    assert type(kspss) == set
