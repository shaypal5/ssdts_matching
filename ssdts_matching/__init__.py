"""Fast matching of source-sharing derivative time series."""

from .core import (
    popping_greedy_timestamp_match,
    greedy_timestamp_match,
    dynamic_timestamp_match,
    hybrid_timestamp_match,
    vertical_aligned_timestamp_match,
    delta_partitioned_timestamp_match
)
