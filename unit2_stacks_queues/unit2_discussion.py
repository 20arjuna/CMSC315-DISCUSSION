"""
===========================================================
UNIT 2 DISCUSSION: STACKS AND QUEUES (PYTHON)
===========================================================

OVERVIEW:
This assignment introduces two fundamental data structures:
the Stack (LIFO) and the Queue (FIFO).

You will complete, modify, and extend the starter code while
explaining key concepts through comments and improved output.
"""

from collections import deque


class EmptyStructureError(IndexError):
    """Raised when removing or viewing an item from an empty stack or queue."""
    pass


class Stack:
    def __init__(self):
        # TODO (Student): Create the internal data structure for the stack.
        # Hint: A Python list can be used to store stack values.
        # The END of the list is the top of the stack, because append() and pop()
        # at the end of a Python list are O(1). Using the front would be O(n).
        self._items = []

    def push(self, value):
        # TODO (Student): Add value to the stack.
        # Add a short comment explaining why this operation supports LIFO behavior.
        # LIFO: every new value goes on top, above everything pushed before it,
        # so it will be the first one pop() reaches.
        self._items.append(value)

    def pop(self):
        # TODO (Student): Remove and return the most recently added value.
        # Improve or explain empty-stack handling.
        # What should happen if the stack is empty?
        # An empty stack raises EmptyStructureError with a clear message instead of
        # returning None, because None could be a real value someone pushed and the
        # caller would not be able to tell "nothing there" apart from "None was stored".
        if self.is_empty():
            raise EmptyStructureError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        # TODO (Student): Return the top value without removing it.
        # Add a comment explaining what peek does.
        # peek() looks at the top (most recent) value but leaves the stack unchanged.
        if self.is_empty():
            raise EmptyStructureError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        # TODO (Student): Return True if the stack has no values.
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        # Shown bottom -> top so the right side is the next value to pop
        return f"Stack(bottom -> top: {self._items})"


class Queue:
    def __init__(self, capacity=None):
        # TODO (Student): Create the internal data structure for the queue.
        # Hint: collections.deque is useful for efficient queue operations.
        # deque gives O(1) appends on the right and O(1) removals on the left.
        # A list would make dequeue O(n), because list.pop(0) shifts every element.
        # capacity is optional. None means the queue can grow without a limit.
        if capacity is not None and (not isinstance(capacity, int) or capacity < 1):
            raise ValueError("capacity must be a positive whole number or None")
        self._items = deque()
        self._capacity = capacity

    def enqueue(self, value):
        # TODO (Student): Add value to the back of the queue.
        # Add a short comment explaining why this operation supports FIFO behavior.
        # FIFO: new values join at the back, behind everything already waiting,
        # so values leave in the same order they arrived.
        if self.is_full():
            raise OverflowError(f"queue is full (capacity {self._capacity})")
        self._items.append(value)

    def dequeue(self):
        # TODO (Student): Remove and return the value from the front of the queue.
        # Explain or improve empty-queue handling.
        # Same reasoning as Stack.pop(): raise a clear error instead of returning None.
        if self.is_empty():
            raise EmptyStructureError("dequeue from an empty queue")
        return self._items.popleft()

    def front(self):
        # TODO (Student): Return the front value without removing it.
        # Add a comment explaining what front returns.
        # front() returns the oldest value, the one that will be dequeued next.
        if self.is_empty():
            raise EmptyStructureError("front of an empty queue")
        return self._items[0]

    def is_empty(self):
        # TODO (Student): Return True if the queue has no values.
        return len(self._items) == 0

    def is_full(self):
        return self._capacity is not None and len(self._items) >= self._capacity

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue(front -> back: {list(self._items)})"


def try_operation(label, operation):
    """Run one operation and print either its result or the error it raised."""
    try:
        result = operation()
        print(f"  {label} -> {result!r}")
    except (EmptyStructureError, OverflowError) as err:
        print(f"  {label} -> {type(err).__name__}: {err}")


# Student scenario: a smart home hub that uses both structures.
#   - A Stack holds the undo history, so "undo" reverses the most recent change first.
#   - A Queue holds incoming device commands, so they run in the order they arrived.
class SmartHomeHub:
    def __init__(self, queue_capacity=5):
        self.settings = {"thermostat": 70, "porch_light": "off", "front_door": "unlocked"}
        self.undo_history = Stack()
        self.command_queue = Queue(capacity=queue_capacity)

    def change_setting(self, device, new_value):
        old_value = self.settings[device]
        self.undo_history.push((device, old_value))    # remember how to reverse it
        self.settings[device] = new_value
        print(f"  set {device}: {old_value!r} -> {new_value!r}")

    def undo(self):
        try:
            device, old_value = self.undo_history.pop()
        except EmptyStructureError:
            print("  undo: nothing left to undo")
            return
        print(f"  undo {device}: {self.settings[device]!r} -> {old_value!r}")
        self.settings[device] = old_value

    def submit(self, device, value):
        try:
            self.command_queue.enqueue((device, value))
            print(f"  queued {device} = {value!r}   (waiting: {len(self.command_queue)})")
        except OverflowError as err:
            print(f"  REJECTED {device} = {value!r}: {err}")

    def process_all(self):
        while not self.command_queue.is_empty():
            device, value = self.command_queue.dequeue()
            self.change_setting(device, value)


def main():
    print("=== UNIT 2: STACKS AND QUEUES ===")

    # ===============================
    # TODO (Student): STACK DEMO
    # ===============================
    # Requirements:
    # 1. Create a Stack object.
    # 2. Add at least 4 values to the stack.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate LIFO behavior.
    # 5. Show what happens when pop() is used on an empty stack.
    #
    # Edge Cases:
    # 6. Show what happens when peek() is used on an empty stack.
    # 7. Create a stack with only one item, remove it,
    #    and verify the stack is empty afterward.

    print("\n=== STACK DEMO ===")
    # Note: in the starter file these print lines were outside main() (no indentation),
    # so they ran at import time. I moved the demo inside main().
    stack = Stack()
    for page in ["home", "products", "cart", "checkout"]:
        stack.push(page)
        print(f"  pushed {page!r:<11} stack is now {stack}")

    print(f"\n  peek() shows the top without removing it: {stack.peek()!r} (size still {len(stack)})")

    print("\n  Popping everything. LIFO means the reverse of the push order:")
    popped = []
    while not stack.is_empty():
        popped.append(stack.pop())
        print(f"  popped {popped[-1]!r:<11} remaining {stack}")
    print(f"  pop order: {popped}")

    print("\n  Empty stack edge cases:")
    try_operation("pop() on empty stack", stack.pop)
    try_operation("peek() on empty stack", stack.peek)

    single = Stack()
    single.push("only item")
    print(f"\n  One-item stack: {single}")
    try_operation("pop()", single.pop)
    print(f"  is_empty() afterward: {single.is_empty()}  len: {len(single)}")

    none_stack = Stack()
    none_stack.push(None)
    print(f"\n  A stack holding None is not empty: is_empty()={none_stack.is_empty()}, pop()={none_stack.pop()!r}")

    # ===============================
    # TODO (Student): QUEUE DEMO
    # ===============================
    # Requirements:
    # 1. Create a Queue object.
    # 2. Add at least 4 values to the queue.
    # 3. Improve the print statements so they clearly explain what is happening.
    # 4. Demonstrate FIFO behavior.
    # 5. Show what happens when dequeue() is used on an empty queue.
    #
    # Edge Cases:
    # 6. Show what happens when front() is used on an empty queue.
    # 7. Create a queue with only one item, remove it,
    #    and verify the queue is empty afterward.

    print("\n=== QUEUE DEMO ===")
    queue = Queue()
    for customer in ["Ava", "Ben", "Cara", "Dev"]:
        queue.enqueue(customer)
        print(f"  enqueued {customer!r:<7} queue is now {queue}")

    print(f"\n  front() shows who is next without removing them: {queue.front()!r} (size still {len(queue)})")

    print("\n  Dequeuing everything. FIFO means the same order they arrived:")
    served = []
    while not queue.is_empty():
        served.append(queue.dequeue())
        print(f"  served {served[-1]!r:<7} remaining {queue}")
    print(f"  serve order: {served}")

    print("\n  Empty queue edge cases:")
    try_operation("dequeue() on empty queue", queue.dequeue)
    try_operation("front() on empty queue", queue.front)

    single_q = Queue()
    single_q.enqueue("only item")
    print(f"\n  One-item queue: {single_q}")
    try_operation("dequeue()", single_q.dequeue)
    print(f"  is_empty() afterward: {single_q.is_empty()}  len: {len(single_q)}")

    print("\n  Boundary condition: a queue with capacity 2")
    small = Queue(capacity=2)
    try_operation("enqueue('a')", lambda: small.enqueue("a"))
    try_operation("enqueue('b')", lambda: small.enqueue("b"))
    try_operation("enqueue('c') when full", lambda: small.enqueue("c"))
    print(f"  queue unchanged after the rejected add: {small}")
    try:
        Queue(capacity=0)
    except ValueError as err:
        print(f"  Queue(capacity=0) rejected: {err}")

    # ===============================
    # Student scenario: smart home hub
    # ===============================
    print("\n=== SCENARIO: SMART HOME HUB ===")
    hub = SmartHomeHub(queue_capacity=4)

    print("Commands arrive from the phone app and wait in a FIFO queue:")
    hub.submit("thermostat", 72)
    hub.submit("porch_light", "on")
    hub.submit("front_door", "locked")
    hub.submit("thermostat", 68)
    hub.submit("porch_light", "off")    # 5th command, queue capacity is 4

    print("\nProcessing the queue in arrival order (each change is pushed onto the undo stack):")
    hub.process_all()
    print(f"  settings now: {hub.settings}")
    print(f"  undo history: {hub.undo_history}")

    print("\nUndo twice. LIFO reverses the most recent change first:")
    hub.undo()
    hub.undo()
    print(f"  settings now: {hub.settings}")

    print("\nUndo until the history runs out:")
    for _ in range(3):
        hub.undo()
    print(f"  settings back to the start: {hub.settings}")


if __name__ == "__main__":
    main()
