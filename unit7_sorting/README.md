# Unit 7 Discussion: Sorting Algorithms

## Overview

For this unit I implemented bubble sort and merge sort in Python, sorted two datasets with both, counted the comparisons each made on random lists from 10 to 3,000 items, tested edge cases, and used both to sort a smart home alert log by severity, continuing my theme from the earlier units.

Run it with:

```
python3 unit7_discussion.py
```

## What I Implemented

### `bubble_sort(lst, key)`
- Copied the list, then made passes that compared each pair of neighbors and swapped them when the left one was larger. After each pass the largest remaining value had moved to the end, so each pass skipped the items already in place.
- Stopped early when a full pass made no swaps, which meant the list was already sorted.
- Only swapped on strictly greater, so equal items never changed order, which makes it stable.
- Worst case n(n-1)/2 comparisons, O(n^2). Best case, an already sorted list, is one pass, O(n).

### `merge_sort(lst, key)` and `merge(left, right, key)`
- Recursively split the list in half until each piece had 0 or 1 items, then merged the sorted halves back together.
- `merge` compared the front items of the two sorted halves, took the smaller one each time, and appended whatever remained when one half ran out. It used `<=` so ties took from the left half, which keeps merge sort stable.
- The list is halved about log2(n) times and each level touches all n items, so merge sort is O(n log n) in every case. It needs O(n) extra memory for the merged lists.

Both functions take an optional `key` so they can sort records by one field, and both count comparisons in a global `comparisons` counter.

## Results

| n | bubble comparisons | merge comparisons | ratio | bubble ms | merge ms |
|---|---|---|---|---|---|
| 10 | 39 | 23 | 1.7x | 0.0 | 0.0 |
| 100 | 4,926 | 542 | 9.1x | 0.6 | 0.1 |
| 1,000 | 498,871 | 8,715 | 57.2x | 70.7 | 1.9 |
| 3,000 | 4,494,889 | 30,911 | 145.4x | 673.1 | 6.5 |

Going from 100 to 1,000 items made bubble sort do about 100 times more comparisons, while merge sort did about 16 times more. Both sorts matched Python's `sorted()` on every dataset.

## Edge Cases
- **Empty list and single element:** both returned the list with 0 comparisons.
- **Already sorted:** bubble sort's early exit stopped after one pass, 7 comparisons, while merge sort still split and merged everything, 12 comparisons. This is the one case where bubble sort won.
- **Reverse sorted:** bubble sort's worst case, 28 comparisons for 8 items, against 12 for merge sort.
- **Duplicates:** both kept every copy and sorted correctly.
- **Original list:** both sorts worked on copies, so the input list was unchanged.

## Student Scenario: Smart Home Alert Log
- Six alerts were stored in time order as `(time, severity, message)` tuples, with severity 1 the most critical.
- Sorting by severity with `key=lambda a: a[1]` grouped the critical alerts first. Because both sorts are stable, alerts with the same severity stayed in time order, so the smoke alert at 07:15 still came before the water leak at 11:30.
- Bubble sort produced exactly the same order, which confirmed both implementations are stable.

## Reflection

This assignment showed me how much the shape of an algorithm matters. Bubble sort only ever fixes neighbors, so on 3,000 random items it made about 4.5 million comparisons, while merge sort's divide-and-conquer approach needed about 31,000. Writing the merge step was the trickiest part. I had to handle one half running out before the other, and I learned that using <= instead of < is what keeps merge sort stable. That turned out to matter for my alert log, where sorting by severity had to keep equal-severity alerts in time order. My edge cases also surprised me. On an already sorted list, bubble sort with an early exit made 7 comparisons and beat merge sort's 12, because merge sort always does the full split and merge. So merge sort is the right default for large or unpredictable data, since it is O(n log n) in every case, but it needs extra memory for the merged lists. Bubble sort only makes sense for tiny lists or data that is already almost sorted, where its early exit makes it close to O(n).
