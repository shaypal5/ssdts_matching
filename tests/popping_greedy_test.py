"""Test the popping_greedy_timestamp_match function."""

import ssdts_matching as ssdts
# from ssdts_matching import popping_greedy_timestamp_match as popping

from .shared import (
    SHORT_SERIES_1,
    SHORT_SERIES_2,
)


def test_popping_1():
    """Test 1 for the popping_greedy_timestamp_match function."""
    res1 = ssdts.popping_greedy_timestamp_match(
        SHORT_SERIES_1, SHORT_SERIES_2, 1)
    assert len(res1) == 2
    assert res1[3] == 3
    assert res1[10] == 10

    res2 = ssdts.popping_greedy_timestamp_match(
        SHORT_SERIES_1, SHORT_SERIES_2, 2)
    assert len(res2) == 5
    assert res2[1] == 2
    assert res2[3] == 3
    assert res2[4] == 5
    assert res2[8] == 7
    assert res2[10] == 10
