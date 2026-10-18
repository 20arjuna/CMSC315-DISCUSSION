"""
===========================================================
Unit 1 DISCUSSION: Python OOP, Namespaces, and Copying
===========================================================

INSTRUCTIONS:
In this assignment, you will build and explore object-oriented programming (OOP) concepts in Python.
You are provided with starter code containing TODO sections. Your task is to complete, modify, and
analyze the code to demonstrate understanding of inheritance, namespaces, and object copying.
"""


from copy import copy, deepcopy


# TODO 1:
# Create a parent class.
#
# Requirements:
# - Include at least one class variable.
# - Include at least two instance variables.
# - Include a constructor (__init__).
# - Include a method that returns or displays information about the object.
#
# Replace the pass statement with your implementation.

class SmartDevice:
    """A generic device on a smart home network."""

    # Class variables are shared by every device
    network_name = "HomeNet"
    device_count = 0

    def __init__(self, name, room):
        # Instance variables are unique to each device.
        # The leading underscore marks them as internal; outside code uses the properties below.
        self._name = name
        self._room = room
        self._is_on = False
        self._event_log = []    # mutable data, used later to show shallow vs deep copy
        SmartDevice.device_count += 1

    @property
    def name(self):
        return self._name

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, new_room):
        # Encapsulation: validate before changing internal state
        if not isinstance(new_room, str) or not new_room.strip():
            raise ValueError("Room must be a non-empty string")
        self._room = new_room.strip()

    def power(self, turn_on):
        self._is_on = bool(turn_on)
        self._event_log.append("power on" if self._is_on else "power off")

    def get_info(self):
        status = "ON" if self._is_on else "OFF"
        return f"{self._name} in {self._room} [{status}] on {self.network_name}"

    # Special methods
    def __str__(self):
        return self.get_info()

    def __repr__(self):
        return f"SmartDevice(name={self._name!r}, room={self._room!r})"

    def __eq__(self, other):
        # Two devices are the same device if they share a name and room
        if not isinstance(other, SmartDevice):
            return NotImplemented
        return (self._name, self._room) == (other._name, other._room)


# TODO 2:
# Create a child class that inherits from the parent class.
#
# Requirements:
# - Use inheritance.
# - Add at least one new class variable.
# - Add at least two new instance variables.
# - Add at least one new method.
# - Override a method from the parent class.
#
# Replace the pass statement with your implementation.

class Thermostat(SmartDevice):
    """A smart thermostat. Inherits name, room, power, and the special methods from SmartDevice."""

    # New class variables: the safe range every thermostat enforces
    MIN_TEMP = 50
    MAX_TEMP = 90

    def __init__(self, name, room, current_temp, target_temp=70):
        super().__init__(name, room)    # reuse the parent's constructor
        self._current_temp = current_temp
        self._target_temp = target_temp
        self.schedule = {"morning": 68, "night": 64}    # nested mutable data

    @property
    def target_temp(self):
        return self._target_temp

    def set_target(self, temp):
        # New method. Rejects bad input instead of storing it.
        if not isinstance(temp, (int, float)) or isinstance(temp, bool):
            raise TypeError(f"Temperature must be a number, got {type(temp).__name__}")
        if not (self.MIN_TEMP <= temp <= self.MAX_TEMP):
            raise ValueError(f"{temp}F is outside the safe range {self.MIN_TEMP}-{self.MAX_TEMP}F")
        self._target_temp = temp
        self._event_log.append(f"target set to {temp}")

    def heating_or_cooling(self):
        if not self._is_on:
            return "idle (device off)"
        if self._current_temp < self._target_temp:
            return "heating"
        if self._current_temp > self._target_temp:
            return "cooling"
        return "holding"

    # Override: extend the parent's info with thermostat details
    def get_info(self):
        base = super().get_info()
        return f"{base} | now {self._current_temp}F, target {self._target_temp}F, {self.heating_or_cooling()}"

    def __repr__(self):
        return (f"Thermostat(name={self._name!r}, room={self._room!r}, "
                f"current_temp={self._current_temp}, target_temp={self._target_temp})")


# TODO 3:
# Create a function that demonstrates class namespaces and instance namespaces.
#
# Your function should:
# - Create at least two objects of the child class.
# - Access a class variable through the class itself.
# - Access the same class variable through an object.
# - Add a new attribute to only one object after it is created.
# - Display each object's namespace using __dict__.
# - Display information about the class namespace.

def demonstrate_namespaces():
    print("\n=== Namespace Demonstration ===")

    upstairs = Thermostat("Upstairs Thermostat", "Hallway", 72)
    basement = Thermostat("Basement Thermostat", "Basement", 61, target_temp=66)

    # The same class variable, reached two ways
    print(f"Thermostat.MAX_TEMP through the class:  {Thermostat.MAX_TEMP}")
    print(f"upstairs.MAX_TEMP through an object:    {upstairs.MAX_TEMP}")
    print(f"network_name lives on the parent class:  {SmartDevice.network_name}")

    # Add an attribute to only one object
    upstairs.nickname = "Big Nest"
    print(f"\nAdded 'nickname' to upstairs only: {upstairs.nickname}")
    print(f"Does basement have 'nickname'? {hasattr(basement, 'nickname')}")

    # Each object's own namespace
    print(f"\nupstairs.__dict__ keys: {list(upstairs.__dict__)}")
    print(f"basement.__dict__ keys: {list(basement.__dict__)}")

    # The class namespace holds methods and class variables, not per-object data
    class_names = [k for k in Thermostat.__dict__ if not k.startswith("__")]
    print(f"\nThermostat.__dict__ (non-dunder): {class_names}")
    print(f"'MAX_TEMP' in upstairs.__dict__? {'MAX_TEMP' in upstairs.__dict__}  (found by lookup on the class)")

    # Assigning through an object creates a shadowing instance attribute; the class is untouched
    basement.MAX_TEMP = 75
    print(f"\nAfter basement.MAX_TEMP = 75:")
    print(f"  basement.MAX_TEMP = {basement.MAX_TEMP} (instance attribute now shadows the class)")
    print(f"  upstairs.MAX_TEMP = {upstairs.MAX_TEMP} (still reads the class variable)")
    print(f"  Thermostat.MAX_TEMP = {Thermostat.MAX_TEMP}")


# TODO 4:
# Create a function that demonstrates shallow copying and deep copying.
#
# Requirements:
# - Create an object that contains nested mutable data.
# - Create a shallow copy.
# - Create a deep copy.
# - Modify the original object's nested data.
# - Display the original object, shallow copy, and deep copy.
# - Use comments to explain the difference between shallow and deep copying.

def demonstrate_copying():
    print("\n=== Copy Demonstration ===")

    original = Thermostat("Living Room Thermostat", "Living Room", 70)
    original.schedule["weekend"] = {"morning": 70, "night": 66}    # dict nested inside a dict

    # A shallow copy builds a new Thermostat object, but its attributes point at the
    # SAME schedule dict and event log list as the original.
    shallow = copy(original)

    # A deep copy recursively copies everything, so it gets its own schedule and log.
    deep = deepcopy(original)

    print(f"original is shallow? {original is shallow}   original is deep? {original is deep}")
    print(f"original.schedule is shallow.schedule? {original.schedule is shallow.schedule}")
    print(f"original.schedule is deep.schedule?    {original.schedule is deep.schedule}")

    # Modify the original's nested data
    original.schedule["weekend"]["morning"] = 74
    original.schedule["night"] = 60
    original.set_target(72)

    print("\nAfter changing the original's weekend morning to 74, night to 60, and target to 72:")
    print(f"  original schedule: {original.schedule}")
    print(f"  shallow schedule:  {shallow.schedule}   <- changed too (shared dict)")
    print(f"  deep schedule:     {deep.schedule}   <- unchanged (independent copy)")

    # _target_temp is an int, which is immutable, so reassigning it on the original
    # never affects either copy. Only shared MUTABLE objects leak between copies.
    print(f"\n  target temps  original={original.target_temp}  shallow={shallow.target_temp}  deep={deep.target_temp}")
    print(f"  event logs    original={original._event_log}  shallow={shallow._event_log}  deep={deep._event_log}")


# TODO 6 (Student extension):
# A SmartHub that manages many devices and handles errors so one bad command
# does not crash the whole system.

class SmartHub:
    def __init__(self, name):
        self.name = name
        self._devices = {}

    def add_device(self, device):
        if not isinstance(device, SmartDevice):
            raise TypeError("Only SmartDevice objects can join the hub")
        if device.name in self._devices:
            raise ValueError(f"A device named {device.name!r} is already registered")
        self._devices[device.name] = device

    def send_command(self, device_name, command, *args):
        """Run a command on one device. Returns True if it worked, False if it failed safely."""
        call = f"{device_name}.{command}({', '.join(repr(a) for a in args)})"
        try:
            device = self._devices[device_name]
            getattr(device, command)(*args)
            print(f"  OK    {call}")
            return True
        except KeyError:
            print(f"  FAIL  no device named {device_name!r}")
        except AttributeError:
            print(f"  FAIL  {device_name} does not support {command!r}")
        except (ValueError, TypeError) as err:
            print(f"  FAIL  {call}: {err}")
        return False

    def __len__(self):
        return len(self._devices)

    def __contains__(self, device_name):
        return device_name in self._devices

    def __iter__(self):
        return iter(self._devices.values())


def demonstrate_hub():
    print("\n=== Student Extension: SmartHub Error Handling ===")
    hub = SmartHub("Main Hub")
    lamp = SmartDevice("Desk Lamp", "Office")
    thermo = Thermostat("Office Thermostat", "Office", 75)
    hub.add_device(lamp)
    hub.add_device(thermo)

    # Duplicate registration is rejected
    try:
        hub.add_device(SmartDevice("Desk Lamp", "Office"))
    except ValueError as err:
        print(f"  Duplicate rejected: {err}")

    print("\nSending a batch of commands, some of them bad:")
    commands = [
        ("Desk Lamp", "power", True),
        ("Office Thermostat", "power", True),
        ("Office Thermostat", "set_target", 68),
        ("Office Thermostat", "set_target", 120),       # out of range
        ("Office Thermostat", "set_target", "warm"),    # wrong type
        ("Desk Lamp", "set_target", 70),                # lamp has no thermostat method
        ("Garage Door", "power", True),                 # device not registered
    ]
    results = [hub.send_command(*cmd) for cmd in commands]
    print(f"\n{sum(results)} of {len(results)} commands succeeded, and the hub is still running.")

    print(f"\nHub has {len(hub)} devices. 'Desk Lamp' in hub? {'Desk Lamp' in hub}")
    for device in hub:
        print(f"  {device}")

    # Edge cases on the parent class itself
    print("\nEdge cases:")
    try:
        lamp.room = "   "
    except ValueError as err:
        print(f"  Blank room rejected: {err}")
    print(f"  Lamp room is still: {lamp.room}")
    print(f"  Same name and room means equal: {lamp == SmartDevice('Desk Lamp', 'Office')}")
    print(f"  Comparing to a non-device: {lamp == 'Desk Lamp'}")
    print(f"  Thermostat turned off reports: {Thermostat('Spare', 'Attic', 80).heating_or_cooling()}")
    empty_hub = SmartHub("Empty Hub")
    print(f"  Empty hub has {len(empty_hub)} devices and lists: {[str(d) for d in empty_hub]}")


# TODO 5:
# Complete the main function.
#
# Requirements:
# - Create at least one object from the parent class.
# - Create at least one object from the child class.
# - Demonstrate inheritance by calling methods.
# - Call your namespace demonstration function.
# - Call your copy demonstration function.

def main():
    print("=== Unit 1 OOP Assignment ===")

    print("\n--- Parent object ---")
    light = SmartDevice("Porch Light", "Front Porch")
    print(light)
    light.power(True)
    print(light)
    print(repr(light))

    print("\n--- Child object ---")
    thermostat = Thermostat("Bedroom Thermostat", "Bedroom", 74, target_temp=70)
    thermostat.power(True)       # inherited from SmartDevice
    print(thermostat)            # __str__ inherited, get_info overridden
    thermostat.set_target(76)    # new method on the child
    print(thermostat)
    print(repr(thermostat))
    print(f"isinstance(thermostat, SmartDevice)? {isinstance(thermostat, SmartDevice)}")
    print(f"Thermostat method resolution order: {[c.__name__ for c in Thermostat.__mro__]}")

    demonstrate_namespaces()
    demonstrate_copying()
    demonstrate_hub()

    # copy() and deepcopy() build objects without calling __init__, so the copies are not counted
    print(f"\nSmartDevice objects created through __init__ this run: {SmartDevice.device_count} (copies are not counted)")


if __name__ == "__main__":
    main()
