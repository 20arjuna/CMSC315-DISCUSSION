# Unit 2 Discussion: Stacks and Queues

## Overview

For this unit I implemented a `Stack` (LIFO) and a `Queue` (FIFO) in Python, tested both with normal use and edge cases, and then used them together in a smart home hub scenario that continued my Unit 1 theme. The hub's undo history was a stack and its incoming command line was a queue.

Run it with:

```
python3 unit2_discussion.py
```

## What I Implemented

### Stack
- Stored values in a Python list with the **end of the list as the top**. `append()` and `pop()` at the end of a list are O(1), while adding or removing at index 0 would have been O(n) because every other element would shift.
- `push()` added to the top, `pop()` removed and returned the top, `peek()` returned the top without removing it, and `is_empty()` checked the length. I also added `__len__` and `__repr__`, with the repr printed bottom to top so the right side was always the next value to pop.
- **Empty handling:** `pop()` and `peek()` on an empty stack raised a custom `EmptyStructureError` (a subclass of `IndexError`) with a clear message. I chose an exception over returning `None` because `None` can be a real stored value, and I tested that a stack holding `None` correctly reported it was not empty.

### Queue
- Stored values in a `collections.deque`. `append()` added to the back and `popleft()` removed from the front, both O(1). A list would have made `dequeue()` O(n) since `list.pop(0)` shifts every remaining element.
- `enqueue()`, `dequeue()`, `front()`, and `is_empty()` followed the same pattern as the stack, with the same `EmptyStructureError` on an empty queue.
- **Capacity (boundary condition):** I added an optional `capacity`. When the queue was full, `enqueue()` raised `OverflowError` and left the queue unchanged. A capacity of 0, a negative number, or a non-integer was rejected when the queue was created. The default of `None` meant no limit.

### Starter file fix
In the starter file, the `STACK DEMO` and `QUEUE DEMO` print lines were not indented, so they sat outside `main()` and ran as soon as the file loaded. I moved both demos inside `main()`.

### Student scenario: SmartHomeHub
- Commands from a phone app were submitted to a **queue** with a capacity of 4, so they ran in the exact order they arrived. The fifth command was rejected with a message instead of crashing the hub.
- Every setting change pushed the old value onto an **undo stack**. Calling `undo()` popped the most recent change and restored it, so changes were reversed newest first. When the history ran out, `undo()` printed "nothing left to undo" instead of raising an error.
- After processing four commands and undoing all of them, every setting was back to its starting value.

## Edge Cases Tested
- `pop()` and `peek()` on an empty stack.
- `dequeue()` and `front()` on an empty queue.
- A one-item stack and a one-item queue, removing the item and confirming `is_empty()` was `True` and the length was 0.
- A stack holding `None`, to confirm an empty check and a stored `None` were not confused.
- Adding to a full queue, and creating a queue with an invalid capacity.
- Undoing with an empty history.

## Why LIFO and FIFO
A stack is LIFO because both adding and removing happen at the same end, the top, so the newest item is always the one on top. That fits undo, a browser's back button, and function calls, where the most recent action is the one you want to reverse or return from first. A queue is FIFO because items are added at one end and removed from the other, so the oldest item is always at the front. That fits a coffee shop line, a print queue, or network packets, where fairness and arrival order matter.

## Memory Growth
Both structures used O(n) memory: each push or enqueue stored one more reference, so memory grew linearly with the number of items. A Python list over-allocated extra slots as it grew, so most `append()` calls were O(1) and only an occasional resize copied the whole list, which made pushes amortized O(1). A `deque` stored items in fixed-size blocks linked together, so it grew one block at a time and never had to copy everything. The capacity option on my queue put a hard upper bound on memory, which is how real systems protect themselves from a flood of requests.

## Sample Output (excerpt)
```
=== SCENARIO: SMART HOME HUB ===
Commands arrive from the phone app and wait in a FIFO queue:
  queued thermostat = 72   (waiting: 1)
  queued porch_light = 'on'   (waiting: 2)
  queued front_door = 'locked'   (waiting: 3)
  queued thermostat = 68   (waiting: 4)
  REJECTED porch_light = 'off': queue is full (capacity 4)

Processing the queue in arrival order (each change is pushed onto the undo stack):
  set thermostat: 70 -> 72
  set porch_light: 'off' -> 'on'
  set front_door: 'unlocked' -> 'locked'
  set thermostat: 72 -> 68

Undo twice. LIFO reverses the most recent change first:
  undo thermostat: 68 -> 72
  undo front_door: 'locked' -> 'unlocked'
```

## Reflection

This assignment showed me that a stack and a queue can store exactly the same data and still behave completely differently, depending only on which end items leave from. I also learned why the underlying container matters, since a list is fast at its end but slow at its front, which is why the queue used a deque. One challenge was deciding what an empty pop should do. Returning None seemed simpler, but I realized None could be a real stored value, so I raised a clear custom error instead and tested a stack holding None to prove the difference. I also found that the starter's demo prints sat outside main() and ran on import, so I moved them inside. In real applications, a stack fits anything that needs to be reversed, like undo or a back button, because the newest action comes off first. A queue fits anything that needs to be fair, like a line of customers or commands to a device, because the oldest request is handled first. My hub used both: the queue kept commands in order and the stack let me undo them newest first.
