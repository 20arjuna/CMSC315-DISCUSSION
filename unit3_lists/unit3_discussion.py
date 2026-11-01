"""
==================================================
Unit 3 DISCUSSION: List Operations (Insert, Delete, Search)
==================================================

INSTRUCTIONS:
This assignment focuses on understanding how lists behave when elements
are inserted, removed, and searched. You will analyze how Python lists
shift elements in memory and how different operations impact performance.
"""


def insert_at(lst, index, value):
    """
    TODO (Student):
    Insert a value into the list at the specified index.

    Requirements:
    - Use a list operation to insert the value.
    - Add comments explaining what happens to existing elements
      after an insertion occurs.
    - Use comments to explain how insertion performance may vary depending on
      where the insertion occurs.
    """
    # A Python list stores its items in one continuous block of memory, so to
    # make room at `index`, every item from `index` to the end moves one slot
    # to the right before the new value is written into the gap.
    #
    # Performance depends on where the insert happens:
    #   - at the end (index == len(lst)) nothing has to move, so it is O(1)
    #     (amortized, because the list occasionally resizes)
    #   - in the middle about half the items move, which is O(n)
    #   - at the beginning every item moves, which is the worst case, O(n)
    #
    # list.insert() also accepts out-of-range indexes without an error: anything
    # past the end appends and anything below -len(lst) goes to the front.
    lst.insert(index, value)


def delete_at(lst, index):
    """
    TODO (Student):
    Remove and return the value at the specified index.

    Requirements:
    - Validate that the index exists.
    - Return the removed value.
    - Return None if the index is invalid.
    - Add comments explaining why index validation and safe deletion are important.
    """
    # Without this check, lst.pop(index) raises IndexError on a bad index (or an
    # empty list) and the whole program stops. Validating first lets the caller
    # get a predictable result (None) and decide what to do instead of crashing.
    # I only accept non-negative indexes so that -1 is not silently treated as
    # "the last item" when it was really a mistake, like a failed search result.
    if not isinstance(index, int) or index < 0 or index >= len(lst):
        return None

    # pop(index) removes the item and shifts every item after it one slot to the
    # left to close the gap. Like insertion, deleting at the end is O(1) and
    # deleting at the front is the worst case, O(n).
    return lst.pop(index)


def search_value(lst, value):
    """
    TODO (Student):
    Search for a value within the list.

    Requirements:
    - Return the index if the value is found.
    - Return -1 if the value is not found.
    - Add comments explaining why this is a linear search and why it scans sequentially.
    """
    # This is a linear search. The list is not sorted, so there is no way to
    # know where a value might be or to skip part of the list. The only safe
    # approach is to check each item in order, starting at index 0.
    #
    # Best case: the value is first, 1 comparison, O(1).
    # Worst case: the value is last or missing, n comparisons, O(n).
    # A missing value is always the worst case, because every item has to be
    # checked before we can say it is not there.
    for i, item in enumerate(lst):
        if item == value:
            return i    # stop at the first match
    return -1


def show(label, lst):
    print(f"  {label:<34} {lst}")


# Student scenario: a smart home "good night" routine.
# The hub runs the steps of a routine in list order, so the position of each
# step matters. Inserting, removing, and finding steps are exactly the list
# operations above.
class Routine:
    def __init__(self, name, steps):
        self.name = name
        self.steps = list(steps)    # copy so the caller's list is not changed

    def add_step(self, step, before=None):
        """Add a step at the end, or right before an existing step."""
        if before is None:
            insert_at(self.steps, len(self.steps), step)    # O(1), nothing shifts
            print(f"  added {step!r} at the end")
            return
        position = search_value(self.steps, before)
        if position == -1:
            print(f"  could not add {step!r}: no step named {before!r}")
            return
        insert_at(self.steps, position, step)    # later steps shift right
        print(f"  added {step!r} before {before!r} (position {position})")

    def remove_step(self, step):
        position = search_value(self.steps, step)
        removed = delete_at(self.steps, position)    # -1 is rejected safely
        if removed is None:
            print(f"  could not remove {step!r}: it is not in the routine")
        else:
            print(f"  removed {removed!r} from position {position}")

    def run(self):
        print(f"  Running {self.name!r}:")
        if not self.steps:
            print("    (no steps)")
        for number, step in enumerate(self.steps, start=1):
            print(f"    {number}. {step}")


def main():
    print("=== UNIT 3: LIST OPERATIONS ===")

    # ===============================
    # TODO (Student): INSERTION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Create a list containing several values.
    # 2. Display the original list.
    # 3. Test insertion at:
    #    - the beginning
    #    - the middle
    #    - the end
    # 4. Display the list after each insertion.
    # 5. Use comments to explain each step in the implementation.

    print("\n=== INSERTION TESTS ===")
    devices = ["lamp", "thermostat", "camera", "lock"]
    show("Original list:", devices)

    # Beginning: index 0. All 4 existing items shift right one slot (worst case).
    insert_at(devices, 0, "doorbell")
    show("Insert 'doorbell' at index 0:", devices)

    # Middle: index len // 2 = 2. Only the items from index 2 onward shift.
    insert_at(devices, len(devices) // 2, "fan")
    show("Insert 'fan' at index 2 (middle):", devices)

    # End: index len(devices). Nothing shifts, the value is placed after the last item.
    insert_at(devices, len(devices), "speaker")
    show("Insert 'speaker' at the end:", devices)

    # ===============================
    # TODO (Student): DELETION TESTS
    # ===============================
    #
    # Requirements:
    # 1. Delete an item from:
    #    - the beginning
    #    - the middle
    #    - the end
    # 2. Display the removed value.
    # 3. Display the updated list after each deletion.
    # 4. Use comments to clearly explain what is happening in the output.

    print("\n=== DELETION TESTS ===")
    # Beginning: removing index 0 makes every remaining item shift left.
    removed = delete_at(devices, 0)
    print(f"  Removed from index 0: {removed!r}")
    show("List after deleting the beginning:", devices)

    # Middle: index 6 // 2 = 3. Only the items after it shift left to close the gap.
    removed = delete_at(devices, len(devices) // 2)
    print(f"  Removed from index 3 (middle): {removed!r}")
    show("List after deleting the middle:", devices)

    # End: the last index. Nothing after it needs to move, so this is the cheap case.
    removed = delete_at(devices, len(devices) - 1)
    print(f"  Removed from the end: {removed!r}")
    show("List after deleting the end:", devices)

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for a value that exists.
    # 2. Search for a value that does not exist.
    # 3. Display the search results with clear explanations.
    # 4. Use comments to explain each step.

    print("\n=== SEARCH TESTS ===")
    # 'thermostat' exists. The search checks index 0, 1, 2 and stops at the match.
    index = search_value(devices, "thermostat")
    print(f"  search 'thermostat' -> {index}  (found after checking {index + 1} items)")

    # 'garage door' does not exist. Every item is checked before returning -1.
    index = search_value(devices, "garage door")
    print(f"  search 'garage door' -> {index}  (checked all {len(devices)} items, not found)")

    # Duplicates: the search returns the FIRST match only.
    with_duplicate = ["lamp", "fan", "lamp"]
    print(f"  search 'lamp' in {with_duplicate} -> {search_value(with_duplicate, 'lamp')}  (first match only)")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Delete using an invalid index
    # - Search for a missing value
    # - Insert into an empty list
    # - Delete from an empty list
    # - Use comments to explain each edge case.

    print("\n=== EDGE CASES ===")
    # 1. Invalid index: index 10 does not exist, so delete_at returns None
    #    and the list is unchanged instead of raising IndexError.
    print(f"  delete_at(devices, 10) -> {delete_at(devices, 10)!r}")
    show("List unchanged:", devices)

    # 2. A negative index is rejected on purpose, for the reason given in delete_at.
    print(f"  delete_at(devices, -1) -> {delete_at(devices, -1)!r}")

    # 3. Delete from an empty list: every index is invalid when len is 0.
    empty = []
    print(f"  delete_at([], 0) -> {delete_at(empty, 0)!r}")

    # 4. Search an empty list: the loop never runs, so the answer is -1 right away.
    print(f"  search_value([], 'lamp') -> {search_value(empty, 'lamp')}")

    # 5. Insert into an empty list: index 0 is both the beginning and the end.
    insert_at(empty, 0, "lamp")
    show("Insert into empty list at index 0:", empty)

    # 6. Insert past the end: list.insert() appends instead of failing.
    insert_at(empty, 99, "fan")
    show("Insert at index 99 (past the end):", empty)

    # ===============================
    # Student scenario: smart home routine
    # ===============================
    print("\n=== SCENARIO: GOOD NIGHT ROUTINE ===")
    routine = Routine("Good Night", ["lock front door", "turn off lights", "set thermostat to 66"])
    routine.run()

    print("\n  Editing the routine:")
    routine.add_step("arm cameras")                                  # end, no shifting
    routine.add_step("close garage", before="lock front door")       # front, everything shifts
    routine.add_step("start dishwasher", before="set thermostat to 66")
    routine.remove_step("turn off lights")                           # middle
    routine.remove_step("water plants")                              # missing, handled safely
    routine.add_step("dim hallway light", before="open blinds")      # missing anchor
    print()
    routine.run()


if __name__ == "__main__":
    main()
