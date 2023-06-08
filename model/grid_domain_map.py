from model.grid_blocks import GridBlocks
import numpy as np


class GridDomainMap(GridBlocks):

    ROWS_PASSED = 4
    CHAR_VALID = '.'

    def __init__(self,
                 domain: str,
                 map: str,
                 path: str):
        self.domain = domain
        self.map = map
        self.path = path
        array = self.__get_array()
        super().__init__(rows=array.shape[0],
                         cols=array.shape[1])
        self.ndarray = array

    def __get_array(self) -> np.array:
        rows = list()
        file = open(self.path, 'r')
        lines = file.readlines()[self.ROWS_PASSED:]
        for line in lines:
            row = list(line.strip())
            row = [0 if x == self.CHAR_VALID else -1 for x in row]
            rows.append(row)
        file.close()
        return np.array(rows)
