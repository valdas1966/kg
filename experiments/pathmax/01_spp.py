from my_spp import MySPP
from f_utils import u_pickle
from random import randint
import config


li = list()
for i in range(1000):
    rows = randint(5, 20)
    cols = randint(5, 20)
    percent_blocks = randint(10, 30)
    radius_bc = randint(2, 5)
    spp = MySPP(rows, cols, percent_blocks, radius_bc)
    li.append(spp)
    if i % 1000 == 0:
        print(i, rows, cols, percent_blocks, radius_bc)

u_pickle.dump(obj=li, path=config.pickle_spp)
