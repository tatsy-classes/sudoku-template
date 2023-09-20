import os
import re
import glob

import cv2
import numpy as np
import pytest
import colorama
from sudoku import solve
from colorama import Fore

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRA_DIR = os.path.join(CUR_DIR, "extra")
if len(list(os.listdir(EXTRA_DIR))) != 0:
    DATA_DIR = os.path.join(EXTRA_DIR, "data", "sudoku")
else:
    DATA_DIR = os.path.join(CUR_DIR, "data")


def get_test_data():
    levels = [1, 2, 3]
    data = []
    for level in levels:
        jpg_paths = glob.glob(os.path.join(DATA_DIR, "level{:d}/*.jpg".format(level)))
        png_paths = glob.glob(os.path.join(DATA_DIR, "level{:d}/*.png").format(level))
        image_paths = jpg_paths + png_paths
        data.extend([(path, level) for path in image_paths])

    return data


class Sudoku(object):
    def __init__(self, image_path: str, answer_path: str) -> None:
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        num_dict = {str(i): i for i in range(1, 10)}
        with open(answer_path, "r") as f:
            ans_text = f.read()

        ans_chars = re.split(r"[\s]+", ans_text)
        ans_chars = [c for line in ans_chars for c in line]
        ans_chars = [num_dict[c] for c in ans_chars if c != ""]
        self.answer = np.array(ans_chars, dtype="int32").reshape((9, 9))


@pytest.fixture(scope="session")
def score():
    score = np.zeros((1), dtype="int32")
    yield score
    print("\n\n")
    print(Fore.BLUE + "[INFO] Your score:  {:d}".format(score.item()), flush=True, end="")


@pytest.mark.parametrize("image_path, level", get_test_data())
def test_solve(image_path, level, score):
    colorama.init()

    basename = os.path.splitext(image_path)[0]
    answer_path = basename + "_ans.txt"
    sudoku = Sudoku(image_path, answer_path)
    output = solve(sudoku.image)

    assert isinstance(output, np.ndarray), "Return NumPy's NDArray!"
    assert output.dtype == np.int32, "Return NumPy array with int32 data type!"
    assert output.ndim == 2, "#dimensions of NumPy array must be 2!"
    assert output.shape[0] == 9 and output.shape[1] == 9, "Size of the NumPy array must be 9x9!"

    if np.all(output == sudoku.answer):
        score += level
    else:
        pytest.fail("Your output does not match the answer!!")
