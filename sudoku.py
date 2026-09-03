import cv2
import numpy as np
import numpy.typing as npt


def recognize(
    image: npt.NDArray[np.uint8], level: int
) -> npt.NDArray[np.int32]:
    """
    Recognize the original Sudoku problem from an RGB image.

    Inputs:
      image: NumPy array with (H, W, 3) shape. The color channels are in RGB order.
      level: The difficulty level of the problem.

    Output:
      9x9 NumPy array with 32-bit signed integers.
      Use 1-9 for recognized digits and 0 for blank or uncertain cells.
    """
    # 以下、画像から元の数独問題を認識する処理
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return np.zeros((9, 9), dtype=np.int32)


def solve(problem: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
    """
    Solve a Sudoku problem recognized by recognize().

    Input:
      problem: 9x9 NumPy array with 32-bit signed integers.

    Output:
      Completed 9x9 NumPy array with 32-bit signed integers.
    """
    # 以下、認識した問題から数独の完成盤面を求める処理
    return np.zeros((9, 9), dtype=np.int32)
