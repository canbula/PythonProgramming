import sys

sys.path.append(".")

import pytest
from src.boracanbula import statistics


@pytest.mark.parametrize(
    "input, expected",
    [
        ([1, 2, 3, 4, 5], 3),
        ([1, 2, 3, 4, 5, 6], 3.5),
        ([1, 2, 3, 4], 2.5),
        ([1, 2, 3], 2),
        ([1, 2], 1.5),
        ([1], 1),
        ([1, 2, 3, 4, 5, 6, 7], 4),
        ([1, 2, 3, 4, 5, 6, 7, 8], 4.5),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 5),
    ],
)
def test_mean(input, expected):
    assert (
        statistics.mean(input) == expected
    ), f"failed on test_mean with input {input} and expected {expected}"
