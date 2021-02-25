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

