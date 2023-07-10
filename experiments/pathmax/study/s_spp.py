from experiments.pathmax.my_spp import MySPP


spp = MySPP(rows=8, cols=4, percent_blocks=25, radius_bc=2)
for k, v in spp.get_meta().items():
    print(f'{k} = [{v}]')

