import os
import re

import cv2
import numpy as np
import pytest
from sudoku import solve

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

file_paths = [
    "./data/level_1.jpg",
    "./data/level_2.jpg",
    "./data/level_3.jpg",
]

answers = [""] * 3

ans = """
2 3 5 7 9 1 6 4 8
1 6 9 4 2 8 7 5 3
7 4 8 6 3 5 9 2 1
3 9 6 2 7 4 8 1 5
5 2 1 3 8 9 4 6 7
4 8 7 1 5 6 3 9 2
8 5 3 9 6 2 1 7 4
9 7 4 5 1 3 2 8 6
6 1 2 8 4 7 5 3 9
"""

answers = [ans] * len(file_paths)

num_dict = {str(i): i for i in range(1, 10)}


@pytest.mark.parametrize("path, answer", zip(file_paths, answers))
def test_solve(path: str, answer: str):
    image = cv2.imread(os.path.join(CUR_DIR, path), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    actual = solve(image)

    assert isinstance(actual, np.ndarray), "Return NumPy's NDArray!"
    assert actual.dtype == np.int32, "Return NumPy array with int32 data type!"
    assert actual.ndim == 2, "#dimensions of NumPy array must be 2!"
    assert actual.shape[0] == 9 and actual.shape[1] == 9, "Size of the NumPy array must be 9x9!"

    expected = re.split(r"[\s]{1,2}", answer)
    expected = [num_dict[c] for c in expected if c != ""]
    expected = np.array(expected, dtype="int32").reshape((9, 9))

    assert np.all(expected == actual), "Your answer is wrong!!"
