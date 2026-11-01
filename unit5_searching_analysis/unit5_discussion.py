"""
=====================================================
UNIT 5 DISCUSSION: SEARCH ALGORITHMS (LINEAR vs BINARY)
=====================================================

INSTRUCTIONS:
In this assignment, you will implement and analyze two
fundamental search algorithms: linear search and binary search.

You will demonstrate your understanding by modifying the
provided code, running experiments on different dataset sizes,
and clearly explaining your results through code comments
and program output.
"""

import math
import time

# Each search records how many times it compared an item with the target.
# Counting comparisons measures the algorithm itself, while timing also
# depends on the computer, so I report both but rely on the counts.
last_comparisons = 0


def linear_search(lst, target):
    """
    TODO (Student):
    Implement a linear search algorithm.

    Requirements:
    - Search the list from beginning to end.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining why linear search
      has O(n) time complexity.
    """
    global last_comparisons
    last_comparisons = 0
    # Check each position in order. In the worst case (target is last or
    # missing) every one of the n items is compared once, so the number of
    # steps grows in direct proportion to n: O(n). Linear search does not
    # need the list to be sorted, because it never skips anything.
    for i in range(len(lst)):
        last_comparisons += 1
        if lst[i] == target:
            return i
    return -1


def binary_search(lst, target):
    """
    TODO (Student):
    Implement a binary search algorithm.

    Requirements:
    - Assume the list is already sorted.
    - Repeatedly reduce the search space by half.
    - Return the index if the target is found.
    - Return -1 if the target is not found.
    - Add comments explaining how each iteration
      reduces the search space.
    """
    global last_comparisons
    last_comparisons = 0
    # low and high mark the part of the list that could still hold the target.
    # At the start that is the whole list.
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        last_comparisons += 1
        if lst[mid] == target:
            return mid
        if lst[mid] < target:
            # The list is sorted, so everything at or left of mid is too small.
            # Throw that half away: the search space shrinks to (mid, high].
            low = mid + 1
        else:
            # Everything at or right of mid is too large. Keep only [low, mid).
            high = mid - 1
    # low passed high, so the search space is empty and the target is not here.
    # Halving n items reaches empty after about log2(n) + 1 steps: O(log n).
    return -1


def run_both(lst, target, label=None):
    """Run both searches on the same input and print the results side by side."""
    lin_index = linear_search(lst, target)
    lin_steps = last_comparisons
    bin_index = binary_search(lst, target)
    bin_steps = last_comparisons
    name = label if label else repr(target)
    print(f"  {name:<22} linear -> {lin_index:>7} ({lin_steps:>9,} comparisons)   "
          f"binary -> {bin_index:>7} ({bin_steps:>2} comparisons)")
    return lin_steps, bin_steps


def time_search(func, lst, target, repeats):
    """Average wall-clock time of one search, in microseconds."""
    start = time.perf_counter()
    for _ in range(repeats):
        func(lst, target)
    return (time.perf_counter() - start) / repeats * 1_000_000


# Student scenario: a smart home sensor log.
# The hub records a temperature reading every minute, and readings are stored
# in time order, so the list of timestamps is already sorted. That makes binary
# search possible for "what was the temperature at 14:37?"-style questions.
class SensorLog:
    def __init__(self):
        self.minutes = []        # minutes since midnight, always increasing
        self.temperatures = []   # reading at the same index

    def record(self, minute, temperature):
        # Appending in time order keeps the list sorted with no extra work.
        if self.minutes and minute <= self.minutes[-1]:
            raise ValueError("readings must be recorded in time order")
        self.minutes.append(minute)
        self.temperatures.append(temperature)

    def reading_at(self, clock):
        hours, mins = map(int, clock.split(":"))
        index = binary_search(self.minutes, hours * 60 + mins)
        if index == -1:
            return None
        return self.temperatures[index]

    def first_reading_above(self, limit):
        # Temperatures are NOT sorted, so binary search cannot be used here.
        # A linear scan in time order is the only correct choice.
        for i in range(len(self.temperatures)):
            if self.temperatures[i] > limit:
                return self.minutes[i], self.temperatures[i]
        return None


def clock(minute):
    return f"{minute // 60:02d}:{minute % 60:02d}"


def main():
    print("=== UNIT 5: SEARCH ALGORITHMS ===")

    # ===============================
    # TODO (Student): SMALL DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a small sorted dataset.
    # 2. Test both linear search and binary search.
    # 3. Search for:
    #    - a value that exists
    #    - a value that does not exist
    # 4. Use comments to clearly explain the results.

    print("\n=== SMALL DATASET TEST ===")
    small = [3, 8, 15, 21, 34, 42, 57, 63, 71, 88]
    print(f"  data ({len(small)} items): {small}")
    # 57 exists at index 6. Linear checks indexes 0-6 (7 comparisons).
    # Binary checks 34 (mid of 0..9), 63 (mid of 5..9), 42 (mid of 5..6), then 57: 4 comparisons.
    run_both(small, 57)
    # 50 does not exist. Linear must check all 10 items before giving up.
    # Binary narrows the range to nothing after about log2(10) + 1 = 4 comparisons.
    run_both(small, 50)
    # With only 10 items the gap is small, which is why either search is fine here.

    # ===============================
    # TODO (Student): LARGE DATASET
    # ===============================
    #
    # Requirements:
    # 1. Create a much larger sorted dataset.
    # 2. Test both search algorithms.
    # 3. Compare the results.
    # 4. Use comments to explain why binary search becomes more
    #    efficient as datasets grow larger.

    print("\n=== LARGE DATASET TEST ===")
    for n in [1_000, 100_000, 1_000_000]:
        data = list(range(0, 2 * n, 2))   # n sorted even numbers
        print(f"  n = {n:,}  (log2(n) = {math.log2(n):.1f})")
        run_both(data, data[-1], "last item")          # worst case for linear
        run_both(data, 2 * n + 1, "missing (too big)")  # worst case for both
    # Each time n grows by 100x, linear search does 100x more work, but binary
    # search only adds about log2(100) = 6.6 more comparisons. Doubling n adds
    # just one more halving step, which is why the gap keeps widening.

    print("\n  Timing on n = 1,000,000 (searching for the last item):")
    big = list(range(0, 2_000_000, 2))
    lin_us = time_search(linear_search, big, big[-1], 3)
    bin_us = time_search(binary_search, big, big[-1], 1000)
    print(f"    linear: {lin_us:>12,.1f} microseconds per search")
    print(f"    binary: {bin_us:>12,.1f} microseconds per search")
    # The exact times depend on the machine, but the ratio is in the thousands,
    # which matches 1,000,000 comparisons versus 20.

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Single-element list
    # - Value not present
    # - Value at the first position
    # - Value at the last position
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")
    # 1. Empty list: linear's loop never runs. For binary, high = -1 < low = 0,
    #    so the while loop never runs either. Both return -1 with 0 comparisons.
    run_both([], 5, "empty list")
    # 2. Single element: both make exactly one comparison, found or not.
    run_both([7], 7, "single item, found")
    run_both([7], 9, "single item, missing")
    # 3. First position: linear's best case (1 comparison), but binary starts in
    #    the middle and has to work its way down to index 0.
    run_both(small, 3, "first item")
    # 4. Last position: linear's worst case for a value that exists.
    run_both(small, 88, "last item")
    # 5. Unsorted input: binary search assumes sorted data. On an unsorted list
    #    it can miss a value that is really there, while linear still finds it.
    unsorted = [42, 8, 63, 3, 21]
    run_both(unsorted, 3, "unsorted list, 3")
    # 6. Duplicates: linear returns the FIRST match. Binary returns whichever
    #    copy it lands on first, which may not be the first one.
    dupes = [1, 2, 2, 2, 2, 2, 3]
    run_both(dupes, 2, "duplicates of 2")

    # ===============================
    # Student scenario: smart home sensor log
    # ===============================
    print("\n=== SCENARIO: SMART HOME SENSOR LOG ===")
    log = SensorLog()
    # One reading per minute for a full day (1,440 readings), warming in the
    # afternoon and cooling at night.
    for minute in range(24 * 60):
        temp = 66 + round(6 * math.sin((minute - 540) / 1440 * 2 * math.pi), 1)
        log.record(minute, temp)
    print(f"  recorded {len(log.minutes):,} readings, one per minute")

    for t in ["06:00", "14:37", "23:59"]:
        temp = log.reading_at(t)
        print(f"  reading at {t}: {temp}F  (binary search, {last_comparisons} comparisons)")
    print(f"  reading at 25:00: {log.reading_at('25:00')}  (outside the log, binary search returns -1)")

    found = log.first_reading_above(71.5)
    print(f"  first reading above 71.5F: {found[1]}F at {clock(found[0])}  (linear scan, temperatures are unsorted)")

    try:
        log.record(100, 70.0)
    except ValueError as err:
        print(f"  recording an out-of-order reading is rejected: {err}")


if __name__ == "__main__":
    main()
