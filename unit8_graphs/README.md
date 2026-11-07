# Unit 8 Discussion: Breadth-First Search

## Overview

For this unit I implemented breadth-first search in Python on an adjacency-list graph of a smart home mesh network, the final piece of the smart home theme from the earlier units. Devices are nodes, and an edge means two devices are in radio range and can relay messages. I used BFS to find the visit order, each device's hop count from the hub, and the fewest-hop route to a device, then compared it with depth-first traversal and tested edge cases.

Run it with:

```
python3 unit8_discussion.py
```

## What I Implemented

### `bfs(graph, start)`
- Returned an empty list for a start node that is not in the graph instead of raising `KeyError`.
- Used a `deque` as a FIFO queue, so every node one edge from the start was visited before any node two edges away.
- Marked a node as visited when it was added to the queue, not when it was removed, so a node reachable from two neighbors was still queued only once.
- Returned the order in which nodes were visited. Each node and edge is handled once, so BFS runs in O(V + E).

### Helpers built on the same idea
- `bfs_levels` recorded each node's distance in edges from the start.
- `shortest_path` stored each node's parent during BFS and walked the parent links back from the goal to rebuild the fewest-edges route, or returned `None` if the goal was unreachable.
- `dfs` used a stack instead of a queue, for comparison.
- `add_edge` added an undirected edge in both adjacency lists and created missing nodes.

## The Graph
Eight devices with nine radio links, including a triangle between the hub, the living room light, and the thermostat:

```
hub            -> living light, thermostat, front lock
living light   -> hub, kitchen plug, thermostat
thermostat     -> hub, living light, hall sensor
front lock     -> hub, porch cam
kitchen plug   -> living light, garage door
hall sensor    -> thermostat, garage door
porch cam      -> front lock
garage door    -> kitchen plug, hall sensor
```

## Results
- **BFS from the hub:** hub, living light, thermostat, front lock, kitchen plug, hall sensor, porch cam, garage door. Level 1 was the three devices next to the hub, level 2 the next three, and the garage door was alone at level 3.
- **Shortest route to the garage door:** hub, living light, kitchen plug, garage door, 3 hops.
- **DFS from the hub:** hub, living light, kitchen plug, garage door, hall sensor, thermostat, front lock, porch cam. DFS reached the garage door, 3 hops away, before the front lock, which is only 1 hop from the hub.
- **After adding a device and a link:** a backyard light linked to the porch cam joined level 3, and its route was hub, front lock, porch cam, backyard light.

## Edge Cases
- **Different start node:** BFS from the garage door produced a completely different order, because distance is measured from the start.
- **Disconnected device:** an attic sensor with no links was never reached from the hub, and `shortest_path` returned `None`.
- **Missing start node:** `bfs(graph, 'pool pump')` returned `[]`.
- **One-node graph:** returned just `['hub']`.
- **Empty graph:** returned `[]`.
- **Cycles:** the hub, living light, and thermostat triangle did not cause an infinite loop, and every device appeared exactly once.

## Reflection

This assignment showed me how much the choice of queue or stack changes a traversal. With a queue, BFS visited my mesh network level by level, so the order also gave each device's hop count from the hub and the fewest-hop route to any device. With a stack, DFS followed one path as deep as it could, and in my network it reached the garage door, three hops away, before the front lock, which sits right next to the hub. The detail that took the most thought was when to mark a node as visited. Marking it when it is added to the queue, instead of when it is removed, keeps a device that two neighbors can reach from being queued twice, and the visited set is also what stopped the cycle between the hub, living light, and thermostat from looping forever. BFS is the right tool when the closest answer matters, such as routing a smart home command through the fewest relays, finding the fewest connections between people in a social network, or a GPS counting the fewest stops. DFS fits problems that explore one possibility fully before backing up, such as solving a maze, detecting cycles, or walking a folder tree.
