# Unit 4 Discussion: Binary Search Trees

## Overview

For this unit I implemented a Binary Search Tree in Python with recursive insert, search, and in-order traversal, tested it on a balanced tree and on several edge cases, and then used it for a smart home thermostat schedule that continued my theme from the earlier units. The schedule entries were added out of order, and the BST kept them sorted by time.

Run it with:

```
python3 unit4_discussion.py
```

## What I Implemented

### `Node`
- Stored a `value` and `left` and `right` references, both starting as `None`, since every new node starts as a leaf.

### `BST`
- **`insert` / `_insert_recursive`:** compared the new value with the current node, went left if it was smaller and right if it was larger, and created a new `Node` when it reached an empty spot. Each call returned the node reference so every parent was reconnected to its child on the way back up. Duplicates were ignored, and the helper returned whether a node was actually added so `size` only grew for new values.
- **`search` / `_search_recursive`:** followed the same left or right rule and returned `True` on a match or `False` after falling off the tree. I also recorded the path of visited values in `last_path` so the output could show how many nodes each search actually checked.
- **`inorder` / `_inorder_recursive`:** visited the left subtree, then the node, then the right subtree, which produced the values in ascending order.
- **`height`:** an extra recursive method that counted levels, so I could compare a balanced tree with a chain.

## Tests
- **Construction:** inserted `[50, 30, 70, 20, 40, 60, 80, 65]`. The values smaller than 50 went into the left subtree and the larger ones into the right subtree. The tree had 8 nodes and a height of 4.
- **Traversal:** the in-order result was `[20, 30, 40, 50, 60, 65, 70, 80]`, and the program confirmed it matched `sorted(values)`.
- **Search:** 50 was found after visiting 1 node and 65 after visiting 4 (`50 -> 70 -> 60 -> 65`). The missing values 45 and 10 each stopped after 3 nodes, because once the search reached an empty child there was nowhere else the value could be.

## Edge Cases
- An empty tree returned `[]` from the traversal, a height of 0, and `False` from a search without visiting any nodes.
- Inserting 40 a second time returned `False` and left the size at 8.
- A one-node tree had a height of 1 and an in-order result of `[7]`.
- Inserting 10 through 80 in sorted order made every value go right, so the tree became a chain with a height of 8 instead of 4. Searching it for 80 visited all 8 nodes, the same as a linear search.

## Student Scenario: Thermostat Schedule
- Each schedule entry was a `("HH:MM", temperature)` tuple. Tuples compare by their first item, and zero-padded times sort the same way as clock times, so the BST ordered the schedule by time.
- Six entries were added out of order, and the in-order traversal printed them from `00:00` to `22:00`. Adding the `06:30` entry a second time was reported as a duplicate.
- `setting_at(time)` answered "what should the thermostat be set to right now?" by walking down the tree and keeping the latest entry at or before the given time. At `07:15` it returned 68F from the `06:30` entry, and at `05:00` it returned 62F from the `00:00` entry.
- One limitation: because the whole tuple was the key, an entry with the same time but a different temperature would have been stored as a second entry instead of replacing the first. Keying on the time alone and storing the temperature separately would have fixed that.

## Sample Output (excerpt)
```
=== SEARCH TESTS ===
  search(50): found     | visited 1 of 8 nodes: 50
  search(65): found     | visited 4 of 8 nodes: 50 -> 70 -> 60 -> 65
  search(45): not found | visited 3 of 8 nodes: 50 -> 30 -> 40
  search(10): not found | visited 3 of 8 nodes: 50 -> 30 -> 20

=== EDGE CASES ===
  inserted 10..80 in sorted order -> height 8 (the balanced tree above had height 4)
  search(80): found     | visited 8 of 8 nodes: 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> 70 -> 80
```

## Reflection

This assignment taught me how a BST uses one simple rule, smaller values go left and larger values go right, to keep data ordered without ever sorting it. I practiced writing recursive helpers that return the updated node, and I learned why an in-order traversal comes out sorted. My main challenge was the insert helper. It needed to return the node reference so parents stayed connected, but I also wanted to know whether a duplicate was skipped so the size stayed correct. I solved it by returning both the node and a True or False flag. Recording the search path was also useful, because it showed exactly how many nodes each search checked. Compared with a list, where a linear search may check every item, each comparison in a BST skips an entire subtree, so a balanced tree of n values needs about log n steps. A sorted array can also be searched in log n steps, but inserting into it means shifting items, while a BST only adds a leaf. My sorted-order test showed the weakness, though. Inserting 10 through 80 in order built a chain, and the search for 80 checked all 8 nodes.
