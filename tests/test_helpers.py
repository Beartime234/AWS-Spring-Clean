import pytest
from helpers import get_results_dir


def test_get_results_dir():
    print(get_results_dir())
    assert get_results_dir()