#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test file for testing the ScanData object from nearfield.py

Relies on the example beamscanner data file in `data/scan_data.csv`
"""


from pathlib import Path
from typing import Dict, File

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
def example_data(data_dir) -> File:
    with open(data_dir / "example_scan.csv", "r") as read_in:
        return read_in


def test_kaiser_smooth(min_x, max_x, n_x, window_len):
    """Dumb test of kaiser smoothing an array of data"""
    # generate some data
    a = np.linspace(min_x, max_x, n_x)
    b = ScanData.kaiser_smooth(a, 1.0, window_len)

    # just check the lengths, as we assume numpy works!
    assert len(b) == len(a)
