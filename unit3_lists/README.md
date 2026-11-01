# Unit 3 Discussion: List Operations

## Overview

For this unit I implemented insertion, deletion, and linear search on Python lists, tested each one at the beginning, middle, and end of a list, and then used all three in a smart home "Good Night" routine that continued my theme from Units 1 and 2. The routine's steps ran in list order, so where a step was inserted or removed actually mattered.

Run it with:

```
python3 unit3_discussion.py
```

## What I Implemented

### `insert_at(lst, index, value)`
- Used `list.insert()`. Because a Python list stores its items in one continuous block of memory, every item from `index` to the end shifted one slot to the right to make room.
- Inserting at the end was O(1) amortized since nothing shifted, inserting in the middle moved about half the items, and inserting at the front moved every item, the O(n) worst case.
- `list.insert()` does not raise an error for an out-of-range index. Anything past the end was appended, which I showed as an edge case.

### `delete_at(lst, index)`
- Validated the index first and returned `None` for anything invalid, including an empty list, instead of letting `pop()` raise `IndexError` and stop the program.
- I only accepted non-negative indexes. Python treats `-1` as "the last item," so a failed search result of `-1` passed straight into a delete would have silently removed the wrong item. Rejecting it made that mistake visible.
- For a valid index, `pop(index)` removed the value and shifted everything after it one slot left, so deleting at the front was the worst case and deleting at the end was the cheap case.

### `search_value(lst, value)`
- A linear search that checked each item in order starting at index 0 and returned the first matching index, or `-1` if nothing matched.
- It had to be sequential because the list was not sorted, so there was no way to skip any part of it. The best case was O(1) when the value was first, and a missing value was always the worst case, O(n), since every item had to be checked first.

## Tests
- **Insertion:** inserted at index 0, at the middle (`len // 2`), and at `len(lst)`, printing the list after each step.
- **Deletion:** deleted from index 0, the middle, and the last index, printing the removed value and the updated list.
- **Search:** found a value that existed, searched for one that did not, and showed that a list with duplicates returned only the first match.

## Edge Cases
- Deleting with an index past the end returned `None` and left the list unchanged.
- Deleting with `-1` was rejected on purpose.
- Deleting from an empty list returned `None`.
- Searching an empty list returned `-1` right away because the loop never ran.
- Inserting into an empty list at index 0, where the beginning and the end are the same position.
- Inserting at index 99 in a one-item list appended the value instead of failing.

## Student Scenario: Good Night Routine
- A `Routine` class held an ordered list of steps that the hub ran from top to bottom.
- `add_step(step, before=None)` appended to the end by default, or used `search_value` to find an existing step and `insert_at` to place the new step in front of it, shifting the later steps right.
- `remove_step(step)` searched for the step and passed the result to `delete_at`. When the step was missing, the search returned `-1`, `delete_at` rejected it, and the routine printed a message instead of crashing or removing the last step by mistake.
- The run started with 3 steps, added one to the end, one to the front, and one in the middle, removed a middle step, and safely handled a missing step and a missing anchor, ending with 5 steps in the right order.

## Sample Output (excerpt)
```
=== INSERTION TESTS ===
  Original list:                     ['lamp', 'thermostat', 'camera', 'lock']
  Insert 'doorbell' at index 0:      ['doorbell', 'lamp', 'thermostat', 'camera', 'lock']
  Insert 'fan' at index 2 (middle):  ['doorbell', 'lamp', 'fan', 'thermostat', 'camera', 'lock']
  Insert 'speaker' at the end:       ['doorbell', 'lamp', 'fan', 'thermostat', 'camera', 'lock', 'speaker']

=== SCENARIO: GOOD NIGHT ROUTINE ===
  added 'arm cameras' at the end
  added 'close garage' before 'lock front door' (position 0)
  added 'start dishwasher' before 'set thermostat to 66' (position 3)
  removed 'turn off lights' from position 2
  could not remove 'water plants': it is not in the routine
  could not add 'dim hallway light': no step named 'open blinds'
```

## Reflection

This assignment showed me that a Python list is one block of memory in a fixed order, so the cost of an insert or delete depends on how many items have to shift to keep that order. Adding or removing at the end moved nothing, while doing the same at index 0 moved every item. I also learned why searching an unsorted list has to be linear, since nothing about the order tells you where a value might be. One challenge was that my first run reported "camera" as not found, even though it was in my original list. The middle deletion had already removed it, so the search was correct and my test was wrong. Tracing the list after each step showed me that each operation changes what the next one sees. I also chose to reject negative indexes in delete_at, because a failed search returns -1 and Python would have deleted the last item instead. In real applications, these costs add up quickly. A playlist or task list that is always edited at the front does O(n) work on every change, so it is better to add at the end or use a deque.
