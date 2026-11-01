"""
=========================================================
UNIT 4 DISCUSSION: BINARY SEARCH TREES (BST)
=========================================================

INSTRUCTIONS:
This assignment focuses on understanding and implementing a
Binary Search Tree (BST).

You will complete and modify the provided code while explaining
key concepts in your own words using comments and output.
"""


class Node:
    def __init__(self, value):
        # TODO (Student):
        # Store the node's value and initialize references
        # to the left and right child nodes.
        # A new node is always a leaf, so both children start as None.
        self.value = value
        self.left = None     # subtree of values smaller than self.value
        self.right = None    # subtree of values larger than self.value


class BST:
    def __init__(self):
        # TODO (Student):
        # Initialize an empty Binary Search Tree.
        # An empty tree has no root node. size counts the values stored, and
        # last_path records the values visited by the most recent search.
        self.root = None
        self.size = 0
        self.last_path = []

    def insert(self, value):
        """
        TODO (Student):
        Insert a value into the BST.

        Requirements:
        - Use the recursive helper method.
        - Add comments explaining why insertion depends on
          whether a value is smaller or larger than the
          current node.
        """
        # Insertion has to follow the same rule every search will follow later:
        # smaller values go left and larger values go right. If a value were
        # placed anywhere else, a search would go the wrong way and miss it.
        # Duplicates are ignored, so each value appears in the tree once.
        # The helper returns True only when a new node was actually created.
        self.root, added = self._insert_recursive(self.root, value)
        if added:
            self.size += 1
        return added

    def _insert_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST insertion.

        Requirements:
        - Create a new node when a position is found.
        - Insert smaller values into the left subtree.
        - Insert larger values into the right subtree.
        - Return the updated node reference.
        """
        if node is None:
            # Reached an empty spot, which is exactly where the value belongs.
            return Node(value), True
        if value < node.value:
            node.left, added = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right, added = self._insert_recursive(node.right, value)
        else:
            added = False    # duplicate, leave the tree unchanged
        # Returning the same node reference reconnects each parent to its child
        # on the way back up, so only the new leaf is actually changed.
        return node, added

    def search(self, value):
        """
        TODO (Student):
        Search for a value in the BST.

        Requirements:
        - Return True if found.
        - Return False if not found.
        - Add comments explaining why BST search is often
          more efficient than linear search.
        """
        # A linear search may have to check every item, O(n). In a BST, each
        # comparison tells us which side the value must be on, so the whole
        # other subtree is skipped. In a balanced tree that cuts the remaining
        # values roughly in half each step, which is O(log n). The catch is that
        # the tree's shape decides the cost: values inserted in sorted order
        # build a chain, and then search becomes O(n) again.
        self.last_path = []
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """
        TODO (Student):
        Implement recursive BST search.
        """
        if node is None:
            return False    # fell off the tree, so the value is not stored
        self.last_path.append(node.value)
        if value == node.value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)     # skip the right subtree
        return self._search_recursive(node.right, value)        # skip the left subtree

    def inorder(self):
        """
        TODO (Student):
        Return a list containing the values from an
        in-order traversal.
        """
        values = []
        self._inorder_recursive(self.root, values)
        return values

    def _inorder_recursive(self, node, values):
        """
        TODO (Student):
        Implement in-order traversal.

        Requirements:
        - Visit the left subtree.
        - Visit the current node.
        - Visit the right subtree.
        - Add comments explaining why this traversal
          produces sorted output in a BST.
        """
        # Every value in the left subtree is smaller than this node and every
        # value in the right subtree is larger. Visiting left, then the node,
        # then right means all smaller values are listed before the node and all
        # larger values after it. That holds at every level, so the full result
        # comes out in ascending order.
        if node is None:
            return
        self._inorder_recursive(node.left, values)
        values.append(node.value)
        self._inorder_recursive(node.right, values)

    def height(self):
        """Number of levels from the root down to the deepest leaf (0 for an empty tree)."""
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))


def report_search(tree, value):
    found = tree.search(value)
    path = " -> ".join(str(v) for v in tree.last_path) or "(no nodes)"
    result = "found" if found else "not found"
    print(f"  search({value!r}): {result:<9} | visited {len(tree.last_path)} of {tree.size} nodes: {path}")


# Student scenario: a smart home thermostat schedule.
# Each entry is (time as "HH:MM", target temperature). Tuples compare by their
# first item, and "HH:MM" strings with leading zeros sort the same way as clock
# times, so the BST keeps the schedule ordered by time.
class ThermostatSchedule:
    def __init__(self):
        self.tree = BST()

    def add(self, time, temperature):
        if not self.tree.insert((time, temperature)):
            print(f"  {time} -> {temperature}F was already in the schedule")

    def show(self):
        # In-order traversal gives the day's changes from earliest to latest.
        for time, temperature in self.tree.inorder():
            print(f"    {time}  set to {temperature}F")

    def setting_at(self, time):
        """Return the most recent temperature set at or before `time`."""
        # Walk down the tree like a search. Whenever a node's time is not after
        # `time`, it is a candidate and anything later is to its right.
        node, best = self.tree.root, None
        while node is not None:
            if node.value[0] <= time:
                best = node.value
                node = node.right
            else:
                node = node.left
        return best


def main():
    print("=== UNIT 4: BINARY SEARCH TREES ===")

    # ===============================
    # TODO (Student): BUILD A TREE
    # ===============================
    #
    # Requirements:
    # 1. Create a BST object.
    # 2. Insert at least 7 values.
    # 3. Include values that go into both left
    #    and right subtrees.
    # 4. Display the values inserted.
    # 5. Use comments to explain why a BST is efficient at reducing search space for each step.

    print("\n=== TREE CONSTRUCTION ===")
    tree = BST()
    values = [50, 30, 70, 20, 40, 60, 80, 65]
    for value in values:
        tree.insert(value)
    print(f"  Inserted in this order: {values}")
    # 50 is the root. 30, 20, 40 are smaller so they went into the left subtree,
    # and 70, 60, 80, 65 are larger so they went into the right subtree.
    # 65: larger than 50 (go right), smaller than 70 (go left), larger than 60
    # (go right). Each comparison ruled out an entire subtree, which is why it
    # took only 3 comparisons to place the 8th value instead of checking all 7.
    print("  Resulting tree:")
    print("              50")
    print("            /    \\")
    print("          30      70")
    print("         /  \\    /  \\")
    print("        20  40  60  80")
    print("                  \\")
    print("                   65")
    print(f"  size: {tree.size}   height: {tree.height()}")

    # ===============================
    # TODO (Student): IN-ORDER TRAVERSAL
    # ===============================
    #
    # Requirements:
    # 1. Perform an in-order traversal.
    # 2. Display the traversal results.
    # 3. Use comments to explain why the traversal produces
    #    sorted output in a BST.

    print("\n=== IN-ORDER TRAVERSAL ===")
    # Left subtree, then the node, then the right subtree. Everything on the
    # left of a node is smaller and everything on the right is larger, so the
    # values come out sorted even though they were inserted out of order.
    result = tree.inorder()
    print(f"  in-order: {result}")
    print(f"  matches sorted(values): {result == sorted(values)}")

    # ===============================
    # TODO (Student): SEARCH TESTS
    # ===============================
    #
    # Requirements:
    # 1. Search for at least two values that exist.
    # 2. Search for at least two values that do not exist.
    # 3. Use comments to clearly explain the results.

    print("\n=== SEARCH TESTS ===")
    # 50 is the root, so it is found with one comparison.
    report_search(tree, 50)
    # 65 is the deepest value: 50 -> 70 -> 60 -> 65, 4 nodes out of 8.
    report_search(tree, 65)
    # 45 is missing. 50 -> 30 -> 40, then 40's right child is empty, so it stops.
    report_search(tree, 45)
    # 10 is missing and smaller than everything. It follows the left edge and stops after 20.
    report_search(tree, 10)

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least one edge case.
    #
    # Example ideas:
    # - Traverse an empty tree
    # - Search an empty tree
    # - Insert duplicate values
    # - Create a tree with only one node
    #
    # Use comments to explain what happens and why.

    print("\n=== EDGE CASES ===")
    # 1. Empty tree: root is None, so traversal returns [] and search returns
    #    False immediately without visiting any node.
    empty = BST()
    print(f"  empty tree in-order: {empty.inorder()}   height: {empty.height()}")
    report_search(empty, 50)

    # 2. Duplicate: 40 is already stored, so insert returns False and the size
    #    stays the same instead of adding a second 40.
    added = tree.insert(40)
    print(f"  insert(40) again -> added={added}, size still {tree.size}")

    # 3. One node: the root is also the only leaf, with no children.
    single = BST()
    single.insert(7)
    print(f"  one-node tree in-order: {single.inorder()}   height: {single.height()}")

    # 4. Sorted insertion order: every value is larger than the last, so each one
    #    goes to the right and the tree becomes a chain. Searching it is no faster
    #    than a linear search.
    chain = BST()
    for value in [10, 20, 30, 40, 50, 60, 70, 80]:
        chain.insert(value)
    print(f"  inserted 10..80 in sorted order -> height {chain.height()} (the balanced tree above had height {tree.height()})")
    report_search(chain, 80)

    # ===============================
    # Student scenario: thermostat schedule
    # ===============================
    print("\n=== SCENARIO: THERMOSTAT SCHEDULE ===")
    schedule = ThermostatSchedule()
    # Added out of order, the way a user might edit the schedule during the week.
    for time, temperature in [("12:00", 70), ("06:30", 68), ("22:00", 64),
                              ("08:00", 66), ("17:30", 71), ("00:00", 62)]:
        schedule.add(time, temperature)
    schedule.add("06:30", 68)    # duplicate entry
    print("  Schedule, read with an in-order traversal:")
    schedule.show()

    print("\n  What should the thermostat be set to right now?")
    for now in ["07:15", "13:45", "23:30", "05:00"]:
        time, temperature = schedule.setting_at(now)
        print(f"    at {now}: {temperature}F (from the {time} entry)")


if __name__ == "__main__":
    main()
