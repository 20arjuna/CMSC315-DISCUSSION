# Unit 6 Discussion: Python Dictionaries as Hash Tables

## Overview

For this unit I used a Python dictionary as a hash table to store smart home thermostat settings, demonstrated insert, lookup, update, and delete, timed lookups against a list as the data grew, tested edge cases, and built a small hash table by hand so collisions could be seen directly. The scenario continued my smart home theme from the earlier units with a device registry keyed by device ID.

Run it with:

```
python3 unit6_discussion.py
```

## What I Demonstrated

### Insert
- Added 5 rooms to an empty dictionary, each mapped to a target temperature. Python hashes each key to an integer, uses it to pick a slot in an internal array, and stores the pair there, so an insert does not depend on how many items are already stored.

### Lookup
- `thermostats['bedroom']` hashed the key, jumped to its slot, and confirmed the stored key matched. `in` used the same lookup.
- Timing showed the difference. Looking up the last key took about 35 nanoseconds whether the dictionary held 1,000 or 1,000,000 items, while checking a list for the same value grew from about 7,000 nanoseconds to about 7,000,000.

### Update
- Assigning a new value to `'bedroom'` replaced only the value. The size stayed at 5, because hash table keys are unique.

### Delete
- `del` removed `'basement'`, and `pop('office')` removed a key and returned its value in one step.

## Edge Cases
- **Missing key with `[]`:** raised `KeyError`.
- **Missing key with `get()`:** returned `None`, or a default such as 65, with no error.
- **Deleting a missing key safely:** `pop('garage', None)` returned `None` instead of raising.
- **"Updating" a missing key:** assigning to a misspelled key, `'livng room'`, silently inserted a new pair instead of updating `'living room'`, which is an easy bug to miss.
- **Empty dictionary:** length 0, `get()` returned `None`, and membership was `False`.
- **Unhashable keys:** a list as a key raised `TypeError: unhashable type: 'list'`, because a list can change after it is stored, which would change its hash. A tuple worked.

## Collisions
A dictionary hides its slots, so I wrote a `ChainedHashTable` that uses `key % bucket_count` and stores colliding keys in a list in the same bucket. With 5 buckets, four of my six device IDs (101, 306, 111, 121) all landed in bucket 1, and finding 121 meant searching a chain of 4. With 7 buckets, the same IDs spread out, the longest chain was 2, and finding 121 checked only 1 item.

## Student Scenario: Smart Home Device Registry
- `DeviceRegistry` stored each device under its ID, such as `"LK-03"`, so a command for any device found it in constant time.
- Registering a duplicate ID was rejected instead of overwriting the existing device.
- Commands for an unknown ID were ignored with a message, using `get()` instead of `[]`.
- Removing a device used `pop(..., None)`, so removing it a second time printed a message instead of crashing.

## Sample Output (excerpt)
```
  Lookup time as the table grows (average of 2,000 lookups of the last key):
    n =     1,000   dict:      34 ns   list:         6,944 ns
    n =   100,000   dict:      34 ns   list:       713,683 ns
    n = 1,000,000   dict:      36 ns   list:     7,128,469 ns

=== COLLISIONS (hand-built table with 5 buckets) ===
  bucket 1: [[101, 'porch light'], [306, 'door lock'], [111, 'garage door'], [121, 'doorbell']]
  bucket 4: [[204, 'thermostat'], [409, 'camera']]

  Same six devices with 7 buckets (a prime number):
  bucket 3: [[101, 'porch light'], [409, 'camera']]
```

## Reflection

This assignment showed me what a dictionary actually does when it stores a key. Python hashes the key to a number, uses that number to pick a slot, and goes straight back to that slot on a lookup, which is why my timing stayed around 35 nanoseconds from 1,000 to 1,000,000 items while a list search grew a thousand times slower. A collision happens when two keys hash to the same slot, and a hash table has to handle it, for example by chaining them in a list. My biggest surprise came from my own collision demo. I picked device IDs I thought were random, but with 5 buckets four of the six landed in bucket 1. I realized key % 5 only depends on the last digit, and three of my IDs ended in 1. Switching to 7 buckets, a prime number, spread them out, and the longest chain dropped from 4 to 2. Hash tables improve efficiency because insert, lookup, and delete are O(1) on average, but that depends on a good hash function and enough buckets. If every key collided, a lookup would be an O(n) scan.
