# Unit 5 Discussion: Search Algorithms

## Overview

For this unit I implemented linear search and binary search in Python, counted how many comparisons each one made on datasets from 10 to 1,000,000 items, tested edge cases, and then used both in a smart home sensor log that continued my theme from the earlier units. The log is sorted by time, so binary search can look up a reading by timestamp, but the temperatures themselves are not sorted, so some questions still need a linear scan.

Run it with:

```
python3 unit5_discussion.py
```

## What I Implemented

### `linear_search(lst, target)`
- Checked each index from 0 to the end and returned the first index that matched, or `-1` if none did.
- The worst case, a target that is last or missing, compares every item once, so the work grows in direct proportion to n: O(n). It works on unsorted data because it never skips anything.

### `binary_search(lst, target)`
- Kept `low` and `high` around the part of the sorted list that could still hold the target, checked the middle item, and threw away the half that could not contain the target. It returned the index on a match, or `-1` once `low` passed `high`.
- Each step halves the search space, so n items run out after about log2(n) + 1 steps: O(log n).

### Measuring the difference
- Both functions record how many comparisons they made in `last_comparisons`. I used comparison counts as the main measurement because they describe the algorithm itself, while timing also depends on the computer. I also timed both on 1,000,000 items as a sanity check.

## Results

| n | linear (last item) | binary (last item) | log2(n) |
|---|---|---|---|
| 10 | 10 | 4 | 3.3 |
| 1,000 | 1,000 | 10 | 10.0 |
| 100,000 | 100,000 | 17 | 16.6 |
| 1,000,000 | 1,000,000 | 20 | 19.9 |

Each time n grew by 100 times, linear search did 100 times more work, while binary search added only about 7 comparisons. On 1,000,000 items, one linear search for the last item took about 48,000 microseconds on my machine and one binary search took about 2 microseconds.

## Edge Cases
- **Empty list:** both returned `-1` with 0 comparisons. For binary search, `high` starts at -1, so the loop never runs.
- **Single element:** both made exactly 1 comparison, whether the value was there or not.
- **First item:** linear search's best case (1 comparison), but binary search took 3 because it starts in the middle.
- **Last item:** linear search's worst case for a value that exists (10 of 10), while binary search took 4.
- **Unsorted list:** binary search returned `-1` for 3 in `[42, 8, 63, 3, 21]` even though 3 was at index 3. Linear search found it. This shows that binary search is only correct on sorted data.
- **Duplicates:** in `[1, 2, 2, 2, 2, 2, 3]`, linear search returned index 1, the first 2, while binary search returned index 3, the first 2 it happened to land on.

## Student Scenario: Smart Home Sensor Log
- `SensorLog` stored one temperature reading per minute for a full day, 1,440 readings, with the minute and the temperature in parallel lists.
- `record()` only accepted readings in time order and raised `ValueError` for an out-of-order reading, which kept the timestamp list sorted, the one requirement binary search depends on.
- `reading_at("14:37")` converted the clock time to minutes and used binary search, finding any reading in 10 or 11 comparisons instead of up to 1,440. A time outside the log returned `None`.
- `first_reading_above(71.5)` used a linear scan, because the temperatures rise and fall during the day and are not sorted. It found the first reading above 71.5F at 13:31.

## Sample Output (excerpt)
```
=== LARGE DATASET TEST ===
  n = 1,000,000  (log2(n) = 19.9)
  last item              linear ->  999999 (1,000,000 comparisons)   binary ->  999999 (20 comparisons)
  missing (too big)      linear ->      -1 (1,000,000 comparisons)   binary ->      -1 (20 comparisons)

=== EDGE CASE TESTS ===
  unsorted list, 3       linear ->       3 (        4 comparisons)   binary ->      -1 ( 2 comparisons)
  duplicates of 2        linear ->       1 (        2 comparisons)   binary ->       3 ( 1 comparisons)

=== SCENARIO: SMART HOME SENSOR LOG ===
  reading at 14:37: 72.0F  (binary search, 10 comparisons)
  first reading above 71.5F: 71.6F at 13:31  (linear scan, temperatures are unsorted)
```

## Reflection

This assignment taught me how to measure an algorithm instead of just describing it. Counting comparisons made the difference concrete: 1,000,000 for linear search against 20 for binary search, and each 100 times increase in data added only about 7 binary comparisons. I had to be careful with the boundary updates in binary search. Setting low to mid + 1 and high to mid - 1 matters, because using mid instead can loop forever when two items are left. I also traced the search for 57 by hand and wrote 3 comparisons in a comment, but the program counted 4. Retracing it showed I had skipped the step that checks 42, which reminded me to check my reasoning against real output. Binary search is the better choice when the data is large and already sorted, such as timestamps in my sensor log. Linear search is still the right choice for small lists, unsorted data, or data that changes constantly, since sorting first costs more than one scan. My edge cases showed the tradeoff clearly: binary search missed a value in an unsorted list that linear search found.
