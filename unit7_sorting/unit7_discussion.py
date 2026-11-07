"""
===========================================================
UNIT 7 DISCUSSION: SORTING ALGORITHMS (BUBBLE SORT VS MERGE SORT)
===========================================================

STUDENT INSTRUCTIONS:
This project explores two fundamental sorting algorithms:
- Bubble Sort (iterative, comparison-based)
- Merge Sort (recursive, divide-and-conquer)

Your goal is to demonstrate both your coding ability and your
understanding of algorithm efficiency and behavior.
"""

import random
import time

# Both sorts count how many times they compare two values, which measures the
# algorithm itself rather than the speed of the computer. key lets either sort
# order records by one field, which the smart home scenario uses.
comparisons = 0


def bubble_sort(lst, key=lambda x: x):
    """
    TODO (Student):
    Implement Bubble Sort.

    Requirements:
    - Create a copy of the original list.
    - Compare adjacent elements.
    - Swap elements when they are out of order.
    - Continue until the list is sorted.
    - Return the sorted list.
    - Add meaningful comments.
    """
    global comparisons
    comparisons = 0
    # Work on a copy so the caller's list is not changed.
    result = list(lst)
    n = len(result)
    for pass_number in range(n - 1):
        swapped = False
        # After each pass the largest remaining value has "bubbled" to the end,
        # so the last pass_number items are already in place and can be skipped.
        for i in range(n - 1 - pass_number):
            comparisons += 1
            # Only swap when the left item is strictly greater. Equal items are
            # never swapped, which keeps bubble sort stable.
            if key(result[i]) > key(result[i + 1]):
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        # If a full pass made no swaps, every adjacent pair is in order, so the
        # whole list is sorted and the remaining passes can be skipped.
        if not swapped:
            break
    # Worst case n(n-1)/2 comparisons: O(n^2). Best case (already sorted) is one
    # pass of n-1 comparisons thanks to the early exit: O(n).
    return result


def merge_sort(lst, key=lambda x: x):
    """
    TODO (Student):
    Implement Merge Sort.

    Requirements:
    - Use recursion.
    - Divide the list into smaller halves.
    - Sort each half recursively.
    - Merge the sorted halves together.
    - Return the sorted list.
    - Add meaningful comments.
    """
    global comparisons
    comparisons = 0
    return _merge_sort(list(lst), key)


def _merge_sort(lst, key):
    # Base case: a list of 0 or 1 items is already sorted.
    if len(lst) <= 1:
        return lst
    # Divide: split the list into two halves.
    mid = len(lst) // 2
    # Conquer: sort each half with the same function.
    left = _merge_sort(lst[:mid], key)
    right = _merge_sort(lst[mid:], key)
    # Combine: merge the two sorted halves into one sorted list.
    # The list is halved about log2(n) times and each level of merging touches
    # all n items once, so merge sort is O(n log n) in every case.
    return merge(left, right, key)


def merge(left, right, key=lambda x: x):
    """
    TODO (Student):
    Implement the merge step used by Merge Sort.

    Requirements:
    - Compare values from the left and right lists.
    - Build a new sorted result list.
    - Append any remaining values.
    - Return the merged sorted list.
    - Add meaningful comments.
    """
    global comparisons
    result = []
    i = j = 0
    # Both lists are already sorted, so the smallest remaining value is always at
    # the front of one of them. Compare the two fronts and take the smaller.
    while i < len(left) and j < len(right):
        comparisons += 1
        # <= takes from the left list on a tie, so equal items keep their
        # original order. That makes merge sort stable.
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # One list ran out. Everything left in the other list is larger than what
    # has been merged so far and already in order, so append it as-is.
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def run_both(label, data):
    """Sort the same data with both algorithms and report results and comparisons."""
    b = bubble_sort(data)
    b_count = comparisons
    m = merge_sort(data)
    m_count = comparisons
    print(f"  {label}")
    print(f"    original:    {data}")
    print(f"    bubble sort: {b}  ({b_count} comparisons)")
    print(f"    merge sort:  {m}  ({m_count} comparisons)")
    print(f"    results match each other and sorted(): {b == m == sorted(data)}")
    return b_count, m_count


def main():
    print("=== UNIT 7: SORTING ALGORITHMS ===")

    # ===============================
    # TODO (Student): DATASET #1
    # ===============================
    #
    # Requirements:
    # 1. Create an unsorted list containing at least 7 values.
    # 2. Display the original list.
    # 3. Sort the list using Bubble Sort.
    # 4. Sort the same list using Merge Sort.
    # 5. Clearly label and display all results.

    print("\n=== DATASET #1 ===")
    # Daily energy use of 8 devices, in watt-hours, in no particular order.
    run_both("Device energy use (Wh):", [420, 75, 1300, 15, 260, 980, 40, 610])

    # ===============================
    # TODO (Student): DATASET #2
    # ===============================
    #
    # Requirements:
    # 1. Create a second dataset.
    # 2. Use different values than Dataset #1.
    # 3. Sort using both algorithms.
    # 4. Compare the results.

    print("\n=== DATASET #2 ===")
    # Thermostat readings with decimals and negatives (an outdoor sensor in winter).
    run_both("Temperature readings (F):", [68.5, -3.2, 71.0, 32.0, 69.8, 12.4, -10.0, 55.1, 70.2, 0.0])

    print("\n  Comparisons as the list grows (random data, average of 3 runs):")
    print(f"    {'n':>6} {'bubble':>12} {'merge':>9} {'ratio':>7}   {'bubble ms':>10} {'merge ms':>9}")
    random.seed(315)
    for n in [10, 100, 1_000, 3_000]:
        b_total = m_total = b_time = m_time = 0
        for _ in range(3):
            data = [random.randint(0, 10_000) for _ in range(n)]
            start = time.perf_counter(); bubble_sort(data); b_time += time.perf_counter() - start
            b_total += comparisons
            start = time.perf_counter(); merge_sort(data); m_time += time.perf_counter() - start
            m_total += comparisons
        print(f"    {n:>6,} {b_total // 3:>12,} {m_total // 3:>9,} {b_total / m_total:>6.1f}x   "
              f"{b_time / 3 * 1000:>10.1f} {m_time / 3 * 1000:>9.1f}")
    # Bubble sort's comparisons grow with n squared (10x more data, about 100x
    # more work), while merge sort's grow with n log n (10x more data, about 16x
    # more work at these sizes), so the gap keeps widening.

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Empty list
    # - Already sorted list
    # - Reverse-sorted list
    # - List with duplicate values
    # - Single-element list
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")
    # 1. Empty list: bubble sort's loops never run; merge sort returns at the base case.
    run_both("Empty list:", [])
    # 2. Single element: already sorted, 0 comparisons for both.
    run_both("Single element:", [42])
    # 3. Already sorted: bubble sort's early exit stops after one pass (n-1
    #    comparisons). Merge sort still splits and merges everything.
    run_both("Already sorted:", [1, 2, 3, 4, 5, 6, 7, 8])
    # 4. Reverse sorted: bubble sort's worst case, every pair is swapped, n(n-1)/2.
    run_both("Reverse sorted:", [8, 7, 6, 5, 4, 3, 2, 1])
    # 5. Duplicates: both handle equal values and keep all copies.
    run_both("Duplicates:", [5, 1, 5, 3, 1, 5, 3])
    # 6. The original list is never changed, because both sorts work on a copy.
    original = [3, 1, 2]
    bubble_sort(original)
    merge_sort(original)
    print(f"  Original list after both sorts: {original}  (unchanged)")

    # ===============================
    # Student scenario: smart home event log
    # ===============================
    print("\n=== SCENARIO: SMART HOME ALERT LOG ===")
    # Alerts arrive in time order. The hub wants to show them grouped by
    # severity (1 = critical) while keeping each group in time order. A STABLE
    # sort on severity does exactly that, because alerts with equal severity
    # keep the order they were already in.
    alerts = [
        ("07:02", 3, "porch light left on"),
        ("07:15", 1, "smoke detected in kitchen"),
        ("08:40", 2, "garage door open"),
        ("09:05", 3, "filter change due"),
        ("11:30", 1, "water leak under sink"),
        ("13:12", 2, "front door unlocked"),
    ]
    print("  In time order:")
    for t, sev, msg in alerts:
        print(f"    {t}  severity {sev}  {msg}")
    by_severity = merge_sort(alerts, key=lambda a: a[1])
    print(f"  Sorted by severity with merge sort ({comparisons} comparisons):")
    for t, sev, msg in by_severity:
        print(f"    {t}  severity {sev}  {msg}")
    same = by_severity == bubble_sort(alerts, key=lambda a: a[1])
    print(f"  Bubble sort gives the same order: {same}  (both sorts are stable)")


if __name__ == "__main__":
    main()
