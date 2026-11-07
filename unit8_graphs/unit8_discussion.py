"""
===========================================================
UNIT 8 DISCUSSION: BREADTH-FIRST SEARCH (BFS)
===========================================================

STUDENT INSTRUCTIONS:
This assignment is designed to help you understand how graphs
are traversed using Breadth-First Search (BFS) and how this
applies to real-world systems (e.g., networks, routes,
social connections).

===========================================================
"""

from collections import deque


def bfs(graph, start):
    """
    TODO (Student):
    Implement Breadth-First Search (BFS).

    Requirements:
    - Use a queue to manage traversal order.
    - Track visited nodes to prevent revisiting nodes.
    - Visit nodes level by level.
    - Return the order in which nodes were visited.

    Add comments explaining:
    - Why a queue is used.
    - Why neighbors are added to the queue.
    - How BFS differs from depth-first traversal.
    """
    # A missing start node has nothing to traverse, so return an empty order
    # instead of raising KeyError.
    if start not in graph:
        return []

    order = []
    # visited is a set so "have I seen this node?" is an O(1) check. A node is
    # marked when it is ADDED to the queue, not when it is removed, so a node
    # reachable from two neighbors is still queued only once.
    visited = {start}
    # The queue is what makes BFS breadth-first. It is FIFO, so every node one
    # edge from the start is removed before any node two edges away, which
    # means nodes come out level by level.
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)
        # Each unvisited neighbor is one edge farther from the start than node,
        # so it joins the BACK of the queue and waits until everything at the
        # current distance has been visited.
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Depth-first traversal uses a stack (or recursion) instead. It follows one
    # path as deep as it can before backing up, so it can reach a far node
    # before a close one. BFS always finishes a whole distance level first.
    return order


def bfs_levels(graph, start):
    """Same traversal as bfs(), but records each node's distance (number of edges) from start."""
    if start not in graph:
        return {}
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance


def shortest_path(graph, start, goal):
    """Fewest-edges path from start to goal, found by BFS and rebuilt from parent links."""
    if start not in graph or goal not in graph:
        return None
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            # Walk the parent links back to the start, then reverse.
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    return None    # goal is not reachable from start


def dfs(graph, start):
    """Iterative depth-first traversal with a stack, for comparison with BFS."""
    if start not in graph:
        return []
    order, visited, stack = [], set(), [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # Push neighbors in reverse so they are explored in listed order.
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)
    return order


def add_edge(graph, a, b):
    """Add an undirected edge, creating either node if it does not exist yet."""
    graph.setdefault(a, [])
    graph.setdefault(b, [])
    if b not in graph[a]:
        graph[a].append(b)
    if a not in graph[b]:
        graph[b].append(a)


def show_graph(graph):
    for node, neighbors in graph.items():
        print(f"  {node:<14} -> {', '.join(neighbors) if neighbors else '(no connections)'}")


def show_levels(levels):
    by_level = {}
    for node, d in levels.items():
        by_level.setdefault(d, []).append(node)
    for d in sorted(by_level):
        print(f"    {d} hop(s): {', '.join(by_level[d])}")


def main():
    print("=== UNIT 8: BREADTH-FIRST SEARCH ===")

    # ===============================
    # TODO (Student): CREATE A GRAPH
    # ===============================
    #
    # Requirements:
    # 1. Create a graph using an adjacency list.
    # 2. Include at least 6 nodes.
    # 3. Include multiple connections between nodes.
    # 4. Clearly display the graph structure.
    # 5. Use comments to explain what the nodes and edges represent.

    print("\n=== GRAPH STRUCTURE ===")
    # Smart home mesh network (like Zigbee or Thread). Each node is a device and
    # each edge means two devices are within radio range and can relay messages
    # to each other. The hub can only talk directly to devices next to it, so a
    # message to a far device hops through others. Edges are undirected.
    graph = {}
    for a, b in [("hub", "living light"), ("hub", "thermostat"), ("hub", "front lock"),
                 ("living light", "kitchen plug"), ("living light", "thermostat"),
                 ("thermostat", "hall sensor"), ("front lock", "porch cam"),
                 ("kitchen plug", "garage door"), ("hall sensor", "garage door")]:
        add_edge(graph, a, b)
    show_graph(graph)
    print(f"  {len(graph)} devices, {sum(len(v) for v in graph.values()) // 2} radio links")

    # ===============================
    # TODO (Student): BFS TRAVERSAL
    # ===============================
    #
    # Requirements:
    # 1. Select a starting node.
    # 2. Perform BFS traversal.
    # 3. Display the traversal order.
    # 4. Use comments to explain how BFS visits nodes level by level.
    # 5. Add at least one additional node or edge
    #    and demonstrate the updated traversal.

    print("\n=== BFS TRAVERSAL ===")
    # Starting at the hub, BFS first visits every device one hop away (living
    # light, thermostat, front lock), then every device two hops away, and so on.
    print(f"  BFS from hub: {' -> '.join(bfs(graph, 'hub'))}")
    print("  Hops from the hub (BFS levels):")
    show_levels(bfs_levels(graph, "hub"))
    path = shortest_path(graph, "hub", "garage door")
    print(f"  Fewest-hop route hub -> garage door: {' -> '.join(path)} ({len(path) - 1} hops)")

    # Compare with depth-first traversal from the same start.
    print(f"\n  DFS from hub: {' -> '.join(dfs(graph, 'hub'))}")
    print("  DFS dives down living light -> kitchen plug -> garage door before it ever")
    print("  visits the front lock, which is only one hop from the hub.")

    # Add a new device and a new link, then traverse again.
    print("\n  Adding a backyard light linked to the porch cam, and a new link porch cam <-> garage door:")
    add_edge(graph, "porch cam", "backyard light")
    add_edge(graph, "porch cam", "garage door")
    print(f"  BFS from hub: {' -> '.join(bfs(graph, 'hub'))}")
    show_levels(bfs_levels(graph, "hub"))
    path = shortest_path(graph, "hub", "backyard light")
    print(f"  Route hub -> backyard light: {' -> '.join(path)} ({len(path) - 1} hops)")

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Start from a different node
    # - Use a disconnected graph
    # - Handle a missing start node safely
    # - Graph containing only one node
    # - Empty graph
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASE TESTS ===")
    # 1. A different start node: the order changes because "distance" is measured
    #    from wherever the traversal starts.
    print(f"  BFS from garage door: {' -> '.join(bfs(graph, 'garage door'))}")
    # 2. Disconnected device: a node with no links is never reached from the hub,
    #    so BFS from the hub skips it and no route exists.
    graph["attic sensor"] = []
    order = bfs(graph, "hub")
    print(f"  'attic sensor' has no links; reached from hub? {'attic sensor' in order}")
    print(f"  shortest_path(hub, attic sensor) -> {shortest_path(graph, 'hub', 'attic sensor')}")
    # 3. Missing start node: returns an empty list instead of raising KeyError.
    print(f"  bfs(graph, 'pool pump') -> {bfs(graph, 'pool pump')}")
    # 4. A graph with one node: the start is the only node visited.
    print(f"  one-node graph: {bfs({'hub': []}, 'hub')}")
    # 5. Empty graph: nothing exists, so there is nothing to visit.
    print(f"  empty graph: {bfs({}, 'hub')}")
    # 6. Cycles: hub, living light, and thermostat form a triangle. The visited
    #    set stops BFS from going around it forever, so each device appears once.
    order = bfs(graph, "hub")
    print(f"  every device visited exactly once despite cycles: {len(order) == len(set(order))}")


if __name__ == "__main__":
    main()
