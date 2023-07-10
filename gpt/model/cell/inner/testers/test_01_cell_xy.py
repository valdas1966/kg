import sys
sys.path.append('d:\\kg')
from gpt.model.cell.inner.i_01_cell_xy import CellXY


def test_str():
    cell1 = CellXY(1, 2, "Cell1")
    cell2 = CellXY(1, 2)
    assert str(cell1) == "Cell1(1,2)"
    assert str(cell2) == "(1,2)"


def test_eq():
    cell1 = CellXY(1, 2, "Cell1")
    cell2 = CellXY(1, 2)
    cell3 = CellXY(2, 3, "Cell3")
    cell4 = CellXY(1, 2, "Cell4")

    # Cells are equal if their coordinates are the same.
    assert cell1 == cell4
    assert cell1 == cell2

    # Cells are not equal if their coordinates are different.
    assert cell1 != cell3


def test_lt_gt():
    cell1 = CellXY(1, 2, "Cell1")
    cell2 = CellXY(2, 3, "Cell2")

    assert cell1 < cell2
    assert cell2 > cell1


def test_le_ge():
    cell1 = CellXY(1, 2, "Cell1")
    cell2 = CellXY(1, 2, "Cell2")

    assert cell1 <= cell2
    assert cell1 >= cell2
