#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test file for testing the ScanData object from nearfield.py

Relies on the example beamscanner data file in `data/scan_data.csv`
"""


from pathlib import Path

import numpy as np

import pytest

from python_beamscanner.nearfield import ScanData


@pytest.fixture
def data_dir() -> Path:
    return Path(__file__).parent / "data"


# Fixtures can simply be added as a parameter to the other test or fixture functions to
# expose them. If we had multiple tests that wanted to use the contents of this file,
# we could simply add "loaded_example_values" as a parameter for each test.
@pytest.fixture
def example_filename(data_dir):
    return data_dir / "wSMA240_88-13mm_240GHz.csv"


@pytest.mark.parametrize(
    "min_x, max_x, n_x, window_len",
    [
        # (min_x, max_x, n_x, window_len)
        (5, 10, 20, 5),
        (5, 10, 31, 5),
        (10, 40, 40, 10),
        (0, 1, 81, 20),
    ],
)
def test_kaiser_smooth(min_x, max_x, n_x, window_len):
    """Dumb test of kaiser smoothing an array of data"""
    # generate some data
    a = np.linspace(min_x, max_x, n_x)
    b = ScanData.kaiser_smooth(a, 1.0, window_len)

    # just check the lengths, as we assume numpy works!
    assert len(b) == len(a)


def test_reading_data(example_filename):
    """Test basic reading of data"""
    d = ScanData()
    d.load_csv_data(example_filename)

    assert d.s21.shape == d.cal_data.shape

    assert d.s21.shape[0] == len(d.x_values)
    assert d.s21.shape[1] == len(d.y_values)

    assert d.x_values[1] - d.x_values[0] == d.x_step
    assert d.y_values[1] - d.y_values[0] == d.y_step
    assert d.x_values[0] == d.x_limits[0]
    assert d.x_values[-1] == d.x_limits[1]
    assert d.y_values[0] == d.y_limits[0]
    assert d.y_values[-1] == d.y_limits[1]
