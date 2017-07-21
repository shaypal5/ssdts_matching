"""Fast matching of source-sharing derivative time series."""

from sys import maxsize

from sortedcontainers import SortedList
from numpy import zeros


def popping_greedy_timestamp_match(timestamps1, timestamps2, delta):
    """Tries to match two timestamp series in a greedy fashion. Timestamps are
    popped from their lists as they are matched.

    Runs in O(M*log(N)) where M=len(timestamps1) and M=len(timestamps2). Not
    guarenteed to find an optimal matching error-wise, where the error
    is the sum of differences between matched pairs.

    Arguments
    ---------
    timestamps1 : sortedcontainers.SortedList
        A sorted list of unique integers.
    timestamps2 : sortedcontainers.SortedList
        A sorted list of unique integers.
    delta : int
        The allowed difference between a matched pair of items from the two
        series.

    Returns
    -------
    ts1_to_ts2 : dict
        A mapping of each matched value in the first series to the value in the
        second series it was matched to.
    """
    timestamps1 = timestamps1.copy()
    timestamps2 = timestamps2.copy()
    ts1_to_ts2 = {}
    if len(timestamps1) < 1 or len(timestamps2) < 1:
        return {}
    for timestamp in timestamps1:
        if timestamp in timestamps2:
            ts1_to_ts2[timestamp] = timestamp
            timestamps2.pop(timestamps2.index(timestamp))
        else:
            insert_ix = timestamps2.bisect(timestamp)
            # if there are both larger and smaller series 2 ts than the stamp
            if insert_ix < len(timestamps2):
                closest_larger = timestamps2[insert_ix]
                larger_dif = closest_larger - timestamp
                closest_smaller = timestamps2[insert_ix-1]
                smaller_dif = closest_smaller - timestamp
                if larger_dif < abs(smaller_dif) and larger_dif < delta:
                    ts1_to_ts2[timestamp] = closest_larger
                    timestamps2.pop(insert_ix)
                elif abs(smaller_dif) < delta:
                    ts1_to_ts2[timestamp] = closest_smaller
                    timestamps2.pop(insert_ix-1)
                # else, this timstamp edge can't match to any timestamp from
                # the second series
            else:  # the largest timestamp from the second series is smaller
                   # than current stamp
                try:
                    if timestamp - timestamps2[insert_ix-1] < delta:
                        ts1_to_ts2[timestamp] = timestamps2[insert_ix-1]
                    timestamps2.pop(insert_ix-1)
                except IndexError:
                    pass
    return ts1_to_ts2


def greedy_timestamp_match(timestamps1, timestamps2, delta, pop=False):
    """Tries to match two timestamp series in a greedy fashion.

    Runs in O(M*log(N)) where M=len(timestamps1) and M=len(timestamps2). If the
    resulting match is an injective function from the first series to the
    second one then the solution is optimal error-wise, where the error is the
    sum of differences between matched pairs.

    Arguments
    ---------
    timestamps1 : sortedcontainers.SortedList
        A sorted list of unique integers.
    timestamps2 : sortedcontainers.SortedList
        A sorted list of unique integers.
    delta : int
        The allowed difference between a matched pair of items from the two
        series.

    Returns
    -------
    ts1_to_ts2 : dict
        A mapping of each matched value in the first series to the value in the
        second series it was matched to.
    """
    ts1_to_ts2 = {}
    if len(timestamps1) < 1 or len(timestamps2) < 1:
        return {}
    for timestamp in timestamps1:
        if timestamp in timestamps2:
            ts1_to_ts2[timestamp] = timestamp
        else:
            insert_ix = timestamps2.bisect(timestamp)
            # if there are both larger and smaller series 2 ts than the stamp
            if insert_ix < len(timestamps2):
                closest_larger = timestamps2[insert_ix]
                larger_dif = closest_larger - timestamp
                closest_smaller = timestamps2[insert_ix-1]
                smaller_dif = closest_smaller - timestamp
                if larger_dif < abs(smaller_dif) and larger_dif < delta:
                    ts1_to_ts2[timestamp] = closest_larger
                elif abs(smaller_dif) < delta:
                    ts1_to_ts2[timestamp] = closest_smaller
                # else, this timstamp edge can't match to any timestamp from
                # the second series
            else:  # the largest timestamp from the second series is smaller
                   # than current stamp
                try:
                    if timestamp - timestamps2[insert_ix-1] < delta:
                        ts1_to_ts2[timestamp] = timestamps2[insert_ix-1]
                except IndexError:
                    pass
    return ts1_to_ts2


START = 0
DIAGONAL = 1
UP = 2
LEFT = 4

def dynamic_timestamp_match(timestamps1, timestamps2, delta):
    """Optimally matches two timestamp series using dynamic programming.

    Runs in O(M*N), where M=len(timestamps1) and N=len(timestamps2).
    Guarentees an optimal solution error-wise, where the error is the sum of
    differences between matched pairs.

    Arguments
    ---------
    timestamps1 : list
        A list of integers representing a series of timestamps.
    timestamps2 : list
        A list of integers representing a series of timestamps.
    delta : int
        The allowed delta, in seconds, between a matched timestamp pair.

    Returns
    -------
    ts1_to_ts2 : dict
        A mapping of each matched value in the first series to the value in the
        second series it was matched to.
    """
    #   Matrix shape:
    #    ____M____
    #    |?|...|?|
    #  N |:|...|:|
    #    |?|...|?|
    unmatch_penalty = delta * 10
    M = len(timestamps1)
    N = len(timestamps2)
    scores = zeros((N+1, M+1))
    directions = zeros((N+1, M+1)) # 1=diagonal, 2=up, 4=left, 0=start
    scores[0, 0] = 0
    directions[0, 0] = START
    for i in range(N+1):
        for j in range(M+1):
            if i == 0 and j == 0:
                continue
            min_score = maxsize
            min_direction = START
            if i > 0: # check up
                min_score = scores[i-1, j]
                min_direction = UP
            if j > 0: # check left
                left_score = scores[i, j-1] + unmatch_penalty
                if left_score < min_score:
                    min_score = left_score
                    min_direction = LEFT
                if i > 0: # check diagonal
                    diff = abs(timestamps1[j-1] - timestamps2[i-1])
                    diag_score = scores[i-1, j-1] + diff
                    if diag_score < min_score and diff < delta:
                        min_score = diag_score
                        min_direction = DIAGONAL
            scores[i, j] = min_score
            directions[i, j] = min_direction
    # walking the path
    ts1_to_ts2 = {}
    i = N
    j = M
    next_direction = directions[i, j]
    while next_direction != START:
        if next_direction == DIAGONAL:
            ts1_to_ts2[timestamps1[j-1]] = timestamps2[i-1]
            i -= 1
            j -= 1
        elif next_direction == UP:
            i -= 1
        elif next_direction == LEFT:
            j -= 1
        next_direction = directions[i, j]
    return ts1_to_ts2


# def _print_solution_stats():
#     print('Greedy algorithm worked for {}/{} ({}%) so far.'.format(
#         GREEDY, TOTAL, (GREEDY / TOTAL) * 100))
#     print('Dynamic algorithm worked for {}/{} ({}%) so far.'.format(
        # DYNAMIC, TOTAL, (DYNAMIC / TOTAL) * 100))


def hybrid_timestamp_match(timestamps1, timestamps2, delta):
    """Finds the optimal matching of two timestamps series using both a greedy
    algorithm and a dynamic one.

    Runs in O(M*N), where M=len(timestamps1) and N=len(timestamps2).
    Guarentees an optimal solution error-wise, where the error is the sum of
    differences between matched pairs.

    Arguments
    ---------
    timestamps1 : list
        A list of integers representing a series of timestamps.
    timestamps2 : list
        A list of integers representing a series of timestamps.
    delta : int
        The allowed delta, in seconds, between a matched timestamp pair.

    Returns
    -------
    ts1_to_ts2 : dict
        A mapping of each matched value in the first series to the value in the
        second series it was matched to.
    """
    # start by trying to match with the faster, greedy approach
    ts1_to_ts2 = greedy_timestamp_match(timestamps1, timestamps2, delta)
    dynamic = 0
    greedy = 0
    # if some series1 stamps are matched to the same series2 stamps,
    if len(set(ts1_to_ts2.values())) < len(ts1_to_ts2.values()) or \
            len(ts1_to_ts2.keys()) < len(timestamps1): # or are unmatched...
        # then greedy algo found a sub-optimal solution, so we go dynamic.
        ts1_to_ts2 = dynamic_timestamp_match(timestamps1, timestamps2, delta)
        dynamic += 1
    else: # otherwise, greedy algo found an optimal solution!
        greedy += 1
    return ts1_to_ts2


def vertical_aligned_timestamp_match(timestamps1, timestamps2, delta):
    """Matches two timestamps series by partioning them by verticals (pairs of
    timestamps from both series with identical values) and matching each
    partition using the hybrid approach.

    Runs in O(M*N), where M=len(timestamps1) and N=len(timestamps2). Does not
    guarentee an optimal solution error-wise, where the error is the sum of
    differences between matched pairs.

    Arguments
    ---------
    timestamps1 : list
        A list of integers representing a series of timestamps.
    timestamps2 : list
        A list of integers representing a series of timestamps.
    delta : int
        The allowed delta, in seconds, between a matched timestamp pair.

    Returns
    -------
    ts1_to_ts2 : dict
        A mapping of each matched value in the first series to the value in the
        second series it was matched to.
    """
    if len(timestamps1) < 1 or len(timestamps2) < 1:
        return {}
    ts1_to_ts2 = {}
    ts1_left_tip = -1
    ts2_left_tip = -1
    for i, timestamp in enumerate(timestamps1):
        if timestamp in timestamps2 or i == (len(timestamps1)-1):
            # Updating right tips
            if timestamp in timestamps2:
                ts1_to_ts2[timestamp] = timestamp
                ts2_right_tip = timestamps2.bisect(timestamp) - 1
            else:
                ts2_right_tip = len(timestamps2)
            ts1_right_tip = i
            if (i - ts1_left_tip > 1) or (i == (len(timestamps1)-1)):
                # Sending a sub-problem...
                if i == len(timestamps1) - 1: # we arrived at the edge...
                    ts1_right_tip = i + 1
                    ts2_right_tip = len(timestamps2) + 1
                sub_ts1 = SortedList(timestamps1[ts1_left_tip+1:ts1_right_tip])
                sub_ts2 = SortedList(timestamps2[
                    ts2_left_tip+1:ts2_right_tip])
                sub_ts1_2_ts2 = hybrid_timestamp_match(sub_ts1, sub_ts2, delta)
                ts1_to_ts2.update(sub_ts1_2_ts2)
            ts1_left_tip = ts1_right_tip
            ts2_left_tip = ts2_right_tip
    return ts1_to_ts2


def delta_partitioned_timestamp_match(
        timestamps1, timestamps2, delta, matching_func=None):
    """"Attempts to match the two given series of timestamps by partioning
    the first series into 2*delta-separated buckets, and applying the given
    matching function to each, combining the sub-solution into a matching.

    If the provided matching function yields optimal matchings, than so is the
    matching provided by this function.

    The algorithm is not guarenteed to be symmetric; giving the same two series
    in the opposite order may yield a different matching.

    Arguments
    ---------
    timestamps1 : list
        A list of integers representing a series of timestamps.
    timestamps2 : list
        A list of integers representing a series of timestamps.
    delta : int
        The allowed delta, in seconds, between a matched timestamp pair.
    matching_func : function, optional
        The matching function to use. Defaults to hybrid_timestamp_match.

    Returns
    -------
    ts1_to_ts2 : dict
        A mapping of each matched value in the first series to the value in the
        second series it was matched to.
    """
    if matching_func is None:
        matching_func = hybrid_timestamp_match
    if len(timestamps1) < 1 or len(timestamps2) < 1:
        return {}, len(timestamps1), len(timestamps2)
    # Breaking things up to 2 * delta-seperated buckets...
    ts1_to_ts2 = {}
    ts1_left_tip = 0
    ts1_right_tip = -1
    for i, timestamp in enumerate(timestamps1):
        if i == 0:
            continue
        dist_to_prev = timestamp - timestamps1[i-1]
        if dist_to_prev > 2 * delta + 1 or i == (len(timestamps1)-1):
            # Updating right tip!
            ts1_right_tip = i
            if i == len(timestamps1) - 1: # we arrived at the edge...
                ts1_right_tip = i + 1
            # Sending a sub-problem...
            sub_ts1 = SortedList(timestamps1[ts1_left_tip:ts1_right_tip])
            sub_ts2 = SortedList([
                ts for ts in timestamps2
                if (timestamps1[ts1_left_tip] - ts < delta) or (
                    ts - timestamps1[ts1_right_tip-1] < delta)
            ])
            sub_ts1_to_ts2 = matching_func(sub_ts1, sub_ts2, delta)
            ts1_to_ts2.update(sub_ts1_to_ts2)
            ts1_left_tip = ts1_right_tip
    return ts1_to_ts2
