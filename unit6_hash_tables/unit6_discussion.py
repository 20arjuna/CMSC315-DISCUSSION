"""
====================================================
UNIT 6 DISCUSSION: Python Dictionaries as Hash Tables
====================================================

INSTRUCTIONS:
In this activity, you will work with Python dictionaries
to simulate the behavior of a hash table.

You will modify the provided starter code to demonstrate
common operations and explain key concepts.

Follow all TODO prompts in the code and ensure your output
clearly communicates what your program is doing at each step.

----------------------------------------------------
"""

import time


def show(label, table):
    print(f"  {label:<26} {table}")


# A tiny hash table with chaining, written by hand so the buckets and collisions
# are visible. A Python dict does the same job internally (it uses open
# addressing instead of chaining), but it never shows you its buckets.
class ChainedHashTable:
    def __init__(self, bucket_count=5):
        self.buckets = [[] for _ in range(bucket_count)]

    def _index(self, key):
        # The hash function turns a key into a bucket number. For integer keys,
        # key % bucket_count spreads keys across the buckets.
        return key % len(self.buckets)

    def insert(self, key, value):
        bucket = self.buckets[self._index(key)]
        for pair in bucket:
            if pair[0] == key:          # key already present: update in place
                pair[1] = value
                return "updated"
        collided = len(bucket) > 0      # another key already lives in this bucket
        bucket.append([key, value])
        return "collision, chained" if collided else "empty bucket"

    def get(self, key):
        bucket = self.buckets[self._index(key)]
        for k, v in bucket:             # only this one bucket is searched
            if k == key:
                return v, len(bucket)
        return None, len(bucket)


# Student scenario: a smart home device registry.
# Every device has a unique ID, and the hub needs to find a device's status
# instantly when a command or sensor event arrives, no matter how many devices
# are registered. That is exactly the job of a hash table.
class DeviceRegistry:
    def __init__(self):
        self.devices = {}

    def register(self, device_id, name, status):
        if device_id in self.devices:
            print(f"  {device_id} is already registered as {self.devices[device_id]['name']!r}, not added again")
            return
        self.devices[device_id] = {"name": name, "status": status}
        print(f"  registered {device_id}: {name}")

    def set_status(self, device_id, status):
        device = self.devices.get(device_id)
        if device is None:
            print(f"  ignored command for unknown device {device_id}")
            return
        print(f"  {device['name']}: {device['status']} -> {status}")
        device["status"] = status

    def remove(self, device_id):
        removed = self.devices.pop(device_id, None)
        if removed is None:
            print(f"  nothing to remove for {device_id}")
        else:
            print(f"  removed {device_id} ({removed['name']})")


def main():
    print("=== UNIT 6: DICTIONARIES AS HASH TABLES ===")

    # ===============================
    # TODO (Student): CREATE A HASH TABLE
    # ===============================
    #
    # Requirements:
    # 1. Create an empty dictionary.
    # 2. Add at least 5 key-value pairs.
    # 3. Add comments explaining how a dictionary
    #    behaves like a hash table.
    # 4. Display the contents of the dictionary.

    print("\n=== INSERT OPERATIONS ===")
    # A dict is Python's built-in hash table. When a key is inserted, Python calls
    # hash(key) to get an integer, uses that integer to pick a slot in an internal
    # array, and stores the key and value there. Finding that slot again later
    # takes the same calculation, not a scan, which is why inserts are O(1) on average.
    thermostats = {}
    thermostats["living room"] = 70
    thermostats["bedroom"] = 66
    thermostats["kitchen"] = 68
    thermostats["office"] = 71
    thermostats["basement"] = 62
    show("after 5 inserts:", thermostats)
    print(f"  {len(thermostats)} key-value pairs stored")
    # Since Python 3.7, a dict also remembers insertion order, so printing it
    # lists keys in the order they were added. The hashing is separate from that order.

    # ===============================
    # TODO (Student): LOOKUP OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Retrieve at least two existing keys.
    # 2. Clearly display the lookup results.
    # 3. Add meaningful comments to explain how the lookup works.

    print("\n=== LOOKUP OPERATIONS ===")
    # thermostats["bedroom"] hashes "bedroom", jumps straight to its slot, and
    # compares the stored key to confirm it is the right one. No other keys are
    # checked, so the cost does not grow with the size of the dictionary.
    print(f"  thermostats['bedroom']  -> {thermostats['bedroom']}")
    print(f"  thermostats['office']   -> {thermostats['office']}")
    print(f"  'kitchen' in thermostats -> {'kitchen' in thermostats}   (membership uses the same hash lookup)")

    # To show the lookup cost really stays flat, time one lookup in dictionaries
    # of very different sizes and compare it with searching a list for the same key.
    print("\n  Lookup time as the table grows (average of 2,000 lookups of the last key):")
    for n in [1_000, 100_000, 1_000_000]:
        keys = list(range(n))
        table = dict.fromkeys(keys, "on")
        target = n - 1
        start = time.perf_counter()
        for _ in range(2_000):
            table[target]
        dict_ns = (time.perf_counter() - start) / 2_000 * 1e9
        start = time.perf_counter()
        for _ in range(20):
            target in keys                  # a list membership test is a linear scan
        list_ns = (time.perf_counter() - start) / 20 * 1e9
        print(f"    n = {n:>9,}   dict: {dict_ns:>7,.0f} ns   list: {list_ns:>13,.0f} ns")

    # ===============================
    # TODO (Student): UPDATE OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Update the value associated with an existing key.
    # 2. Display the dictionary before and after the update.
    # 3. Use comments to explain what happens when an existing key is assigned
    #    a new value.

    print("\n=== UPDATE OPERATIONS ===")
    show("before:", thermostats)
    # Assigning to a key that already exists hashes to the same slot, finds the
    # matching key, and replaces only the value. Keys in a hash table are unique,
    # so the dictionary does not grow and the key keeps its original position.
    thermostats["bedroom"] = 64
    show("after bedroom = 64:", thermostats)
    print(f"  size is still {len(thermostats)}")

    # ===============================
    # TODO (Student): DELETE OPERATIONS
    # ===============================
    #
    # Requirements:
    # 1. Delete at least one key-value pair.
    # 2. Display the dictionary before and after deletion.
    # 3. Use comments to explain what happens when a key is removed.

    print("\n=== DELETE OPERATIONS ===")
    show("before:", thermostats)
    # del hashes the key to find its slot and removes the pair. Internally Python
    # marks the slot as "deleted" rather than empty, so lookups for other keys
    # that were placed past this slot during a collision can still be found.
    del thermostats["basement"]
    show("after del basement:", thermostats)
    # pop() removes a key and returns its value in one step.
    office = thermostats.pop("office")
    print(f"  pop('office') returned {office}")
    show("after pop office:", thermostats)

    # ===============================
    # TODO (Student): EDGE CASES
    # ===============================
    #
    # Demonstrate at least two edge cases.
    #
    # Example ideas:
    # - Lookup a missing key
    # - Delete a missing key safely
    # - Update a missing key
    # - Use an empty dictionary
    #
    # Explain what happens in each case.

    print("\n=== EDGE CASES ===")
    # 1. Missing key with []: the hash points to a slot with no matching key,
    #    so Python raises KeyError instead of guessing a value.
    try:
        thermostats["garage"]
    except KeyError as err:
        print(f"  thermostats['garage'] -> KeyError: {err}")
    # 2. Missing key with get(): returns None, or a default I choose, with no error.
    print(f"  thermostats.get('garage')     -> {thermostats.get('garage')}")
    print(f"  thermostats.get('garage', 65) -> {thermostats.get('garage', 65)}")
    # 3. Deleting a missing key safely: pop with a default does nothing and returns
    #    the default, while del would raise KeyError.
    print(f"  thermostats.pop('garage', None) -> {thermostats.pop('garage', None)}")
    # 4. "Updating" a missing key with = does not fail. It silently inserts a new
    #    pair, which can hide a typo, so code that should only update existing
    #    keys has to check first.
    thermostats["livng room"] = 72          # typo on purpose
    show("after typo update:", thermostats)
    print("  a new key was added instead of updating 'living room'")
    del thermostats["livng room"]
    # 5. Empty dictionary: lookups and length still work and nothing is found.
    empty = {}
    print(f"  empty dict: len = {len(empty)}, get('x') = {empty.get('x')}, 'x' in empty = {'x' in empty}")
    # 6. Unhashable keys: a list can change after it is stored, which would change
    #    its hash and lose its slot, so Python refuses to use it as a key.
    try:
        bad = {["porch", "light"]: "on"}
    except TypeError as err:
        print(f"  list as a key -> TypeError: {err}")
    print(f"  tuple as a key works: {{('porch', 'light'): 'on'}} -> {{('porch', 'light'): 'on'}}")

    # ===============================
    # Collisions, made visible
    # ===============================
    print("\n=== COLLISIONS (hand-built table with 5 buckets) ===")
    # A dict hides its slots, so this small table uses key % 5 as the hash function
    # and stores colliding keys in a list in the same bucket (chaining).
    table = ChainedHashTable(bucket_count=5)
    for device_id, name in [(101, "porch light"), (204, "thermostat"), (306, "door lock"),
                            (111, "garage door"), (409, "camera"), (121, "doorbell")]:
        result = table.insert(device_id, name)
        print(f"  insert {device_id} ({name:<11}) -> bucket {device_id % 5}: {result}")
    for i, bucket in enumerate(table.buckets):
        print(f"  bucket {i}: {bucket}")
    value, checked = table.get(121)
    print(f"  get(121) -> {value!r}, but it had to search a bucket of {checked} items")
    # With 5 buckets, key % 5 only depends on the last digit, so every ID ending
    # in 1 or 6 lands in bucket 1 and every ID ending in 4 or 9 lands in bucket 4.
    # Four of six devices pile into one chain while three buckets sit empty.

    print("\n  Same six devices with 7 buckets (a prime number):")
    table7 = ChainedHashTable(bucket_count=7)
    for device_id, name in [(101, "porch light"), (204, "thermostat"), (306, "door lock"),
                            (111, "garage door"), (409, "camera"), (121, "doorbell")]:
        table7.insert(device_id, name)
    for i, bucket in enumerate(table7.buckets):
        print(f"  bucket {i}: {bucket}")
    value, checked = table7.get(121)
    print(f"  get(121) -> {value!r}, searched a bucket of {checked} item(s)")
    # A prime bucket count uses every digit of the key, so the IDs spread out and
    # the longest chain drops from 4 to 2. Short chains keep lookups close to O(1).
    # If every key collided, one bucket would hold everything and a lookup would
    # become an O(n) scan, no better than a list.

    # ===============================
    # Student scenario: smart home device registry
    # ===============================
    print("\n=== SCENARIO: SMART HOME DEVICE REGISTRY ===")
    registry = DeviceRegistry()
    registry.register("LT-01", "porch light", "off")
    registry.register("TH-02", "thermostat", "70F")
    registry.register("LK-03", "front door lock", "unlocked")
    registry.register("LT-01", "duplicate light", "off")        # duplicate ID rejected
    print()
    registry.set_status("LK-03", "locked")
    registry.set_status("LT-01", "on")
    registry.set_status("CM-99", "recording")                    # unknown device
    registry.remove("TH-02")
    registry.remove("TH-02")                                     # already gone
    print()
    for device_id, info in registry.devices.items():
        print(f"  {device_id}: {info['name']} is {info['status']}")


if __name__ == "__main__":
    main()
