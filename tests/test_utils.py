# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from naive_foss_health.scrapers.utils import to_int

import pytest

def test_k():
    assert to_int("1.7k") == 1700

def test_m():
    assert to_int("1.7m") == 1700000

def test_comma():
    assert to_int("1,723") == 1723


