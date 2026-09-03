import glob
import os
from pathlib import Path

import cv2
import numpy as np
import pytest
import numpy.typing as npt

from sudoku import recognize, solve

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR, "data")


def get_test_data() -> dict[int, list[str]]:
    """Collect up to 10 sample images per level with a fixed random order."""
    rng = np.random.RandomState(31415)
    result: dict[int, list[str]] = {}
    for level in (1, 2, 3):
        image_paths = sorted(glob.glob(os.path.join(DATA_DIR, f"level{level:d}/*.jpg")))
        n_samples = min(10, len(image_paths))
        indices = rng.choice(len(image_paths), n_samples, replace=False)
        result[level] = [image_paths[i] for i in indices]
    return result


TEST_DATA = get_test_data()


def load_problem(image_path: str) -> npt.NDArray[np.int32]:
    text_path = Path(image_path).with_suffix(".txt")
    text = text_path.read_text(encoding="utf-8")
    digits = [int(char) for char in text if char in "0123456789"]
    if len(digits) != 81:
        raise ValueError(f"Expected 81 digits in {text_path}, got {len(digits)}")
    return np.asarray(digits, dtype=np.int32).reshape(9, 9)


def load_image(image_path: str) -> npt.NDArray[np.uint8]:
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def validate_board(board: object, *, allow_zero: bool) -> None:
    assert isinstance(board, np.ndarray), "Return NumPy's NDArray!"
    assert board.dtype == np.int32, "Return NumPy array with int32 data type!"
    assert board.shape == (9, 9), "Size of the NumPy array must be 9x9!"
    lower = 0 if allow_zero else 1
    assert np.logical_and(board >= lower, board <= 9).all(), (
        f"Array values must be integers from {lower} to 9!"
    )


def recognition_stats(
    prediction: npt.NDArray[np.int32],
    problem: npt.NDArray[np.int32],
) -> tuple[int, int, int]:
    true_digit = problem != 0
    same = prediction == problem
    tp = int(np.count_nonzero(true_digit & same))
    fp = int(np.count_nonzero((prediction != 0) & ~same))
    fn = int(np.count_nonzero(true_digit & ~same))
    return tp, fp, fn


def check_solution(
    answer: npt.NDArray[np.int32],
    problem: npt.NDArray[np.int32],
) -> tuple[bool, str]:
    if not np.array_equal(answer[problem != 0], problem[problem != 0]):
        return False, "Recognized numbers may be wrong"

    expected = np.arange(1, 10, dtype=np.int32)
    for i in range(9):
        if not np.array_equal(np.sort(answer[i]), expected):
            return False, "A row does not contain all numbers 1-9"
    for j in range(9):
        if not np.array_equal(np.sort(answer[:, j]), expected):
            return False, "A column does not contain all numbers 1-9"
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = answer[i : i + 3, j : j + 3].reshape(-1)
            if not np.array_equal(np.sort(block), expected):
                return False, "A block does not contain all numbers 1-9"
    return True, "Success"


@pytest.mark.parametrize("level", (1, 2, 3))
def test_recognition(level: int) -> None:
    tp = fp = fn = 0
    for image_path in TEST_DATA[level]:
        image = load_image(image_path)
        problem = load_problem(image_path)
        prediction = recognize(image, level)
        validate_board(prediction, allow_zero=True)
        case_tp, case_fp, case_fn = recognition_stats(prediction, problem)
        tp += case_tp
        fp += case_fp
        fn += case_fn

    denominator = 2 * tp + fp + fn
    f1 = 0.0 if denominator == 0 else 2 * tp / denominator
    print(f"Level {level} recognition F1: {f1:.4f} (TP={tp}, FP={fp}, FN={fn})")


@pytest.mark.parametrize(
    "image_path, level",
    [
        (image_path, level)
        for level, image_paths in TEST_DATA.items()
        for image_path in image_paths
    ],
)
def test_final(image_path: str, level: int) -> None:
    image = load_image(image_path)
    problem = load_problem(image_path)
    prediction = recognize(image, level)
    validate_board(prediction, allow_zero=True)

    answer = solve(prediction)
    validate_board(answer, allow_zero=False)
    success, message = check_solution(answer, problem)
    assert success, f"Your answer is wrong: {message}"
