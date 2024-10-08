import cv2
import numpy as np
import numpy.typing as npt


def solve(image: npt.NDArray[np.uint8], level: int) -> npt.NDArray[np.int32]:
    """
    Inputs:
      image: NumPy array with (H, W, 3) shape. The color channels are in RGB order.
      level: The difficulty level of the problem
    Output:
      9x9 NumPy array with 32-bit signed integer
    """
    # 以下、数独の問題を解く処理
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return np.zeros((9, 9), dtype="int32")
