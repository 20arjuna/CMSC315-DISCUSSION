# Unit 1 Discussion: Python OOP, Namespaces, and Copying

## Overview

For this unit I modeled a small smart home network in Python. A parent class, `SmartDevice`, held what every device on the network has in common, and a child class, `Thermostat`, extended it with temperature control. I then used those classes to demonstrate class and instance namespaces, shallow and deep copying, and, as my own extension, a `SmartHub` that sends commands to many devices and handles bad commands without crashing.

Run it with:

```
python3 unit1_discussion.py
```

## What I Implemented

### TODO 1: Parent class (`SmartDevice`)
- Class variables `network_name` and `device_count` were shared by every device. `device_count` was incremented in `__init__`, so it counted every device built through the constructor.
- Instance variables `_name`, `_room`, `_is_on`, and `_event_log` were unique to each object.
- I used encapsulation by keeping the instance data behind a leading underscore and exposing it through `@property` getters. The `room` setter validated its input and raised `ValueError` for a blank room, so an object could not be put into a bad state from outside.
- `get_info()` returned a readable status line, and the special methods `__str__`, `__repr__`, and `__eq__` made the objects print cleanly and compare by name and room. `__eq__` returned `NotImplemented` for non-devices so comparing a device to a string returned `False` instead of crashing.

### TODO 2: Child class (`Thermostat`)
- Inherited from `SmartDevice` and called `super().__init__()` so the parent set up the shared fields.
- Added class variables `MIN_TEMP` and `MAX_TEMP` for the safe range, and instance variables `_current_temp`, `_target_temp`, and a nested `schedule` dictionary.
- Added the new methods `set_target()` and `heating_or_cooling()`. `set_target()` raised `TypeError` for non-numbers (including `True`/`False`, since `bool` is a subclass of `int` in Python) and `ValueError` for temperatures outside 50 to 90F.
- Overrode `get_info()` to call the parent version and append the temperature details, and overrode `__repr__`. `__str__` was inherited unchanged, and because it calls `get_info()`, printing a thermostat automatically used the overridden version.

### TODO 3: Namespaces
- I accessed `MAX_TEMP` through both `Thermostat.MAX_TEMP` and an object and got the same value, because Python looks up an attribute on the instance first and then falls back to the class.
- I added `nickname` to only one thermostat and showed with `hasattr()` and `__dict__` that the other object did not have it.
- I printed `Thermostat.__dict__` to show that methods and class variables live in the class namespace, and confirmed `MAX_TEMP` was not in any instance's `__dict__`.
- I also assigned `basement.MAX_TEMP = 75`, which created an instance attribute that shadowed the class variable for that one object only. The other thermostat and the class itself still read 90.

### TODO 4: Shallow vs. deep copying
- I gave a thermostat a nested schedule (a dictionary inside a dictionary) and made a `copy()` and a `deepcopy()`.
- The output showed `original.schedule is shallow.schedule` was `True` and `original.schedule is deep.schedule` was `False`.
- After I changed the original's nested schedule, the shallow copy showed the same changes because it shared the same dictionary, while the deep copy kept the original values. The shared `_event_log` list behaved the same way.
- Changing the original's target temperature did not affect either copy, because an `int` is immutable and reassigning it replaced the reference on the original only. Only shared mutable objects leaked between copies.

### TODO 5: `main()`
`main()` created a parent object and a child object, called inherited methods (`power()`) and new methods (`set_target()`) on the child, showed that `isinstance(thermostat, SmartDevice)` was `True`, printed the method resolution order (`Thermostat -> SmartDevice -> object`), and then ran every demonstration.

### TODO 6: Student extension (`SmartHub`)
I added a hub that registered devices and sent commands to them by name. `send_command()` wrapped each call in `try/except` and caught four kinds of failure separately: an unknown device (`KeyError`), a command the device did not support (`AttributeError`), and invalid values (`ValueError` and `TypeError`). In a batch of 7 commands, 4 failed and were reported, and the hub kept running and finished the batch. The hub also implemented `__len__`, `__contains__`, and `__iter__`, so it worked with `len(hub)`, `"Desk Lamp" in hub`, and `for device in hub`.

## Edge Cases Tested
- A temperature outside the safe range (120F) and a non-number (`"warm"`) were rejected and the old target was kept.
- A command sent to a device that did not support it, and a command sent to a device that was not registered.
- Registering a device twice was rejected.
- Setting a blank room was rejected and the room stayed unchanged.
- Comparing a device to a non-device returned `False`.
- A thermostat that was off reported `idle` instead of heating or cooling.
- An empty hub returned a length of 0 and iterated over nothing without errors.

## Memory Behavior
Every object stored its own data in its own `__dict__`, so memory grew with each device created, while class variables and methods were stored once on the class no matter how many objects existed. Adding an attribute to one object (like `nickname`) grew only that object's dictionary. A shallow copy was cheap because it created one new object that pointed at the existing nested data, but that sharing was also what caused changes to leak. A deep copy cost more memory and time because it recursively duplicated every nested structure, and the cost grew with how deeply nested the data was. I also noticed that `copy()` and `deepcopy()` did not call `__init__`, so `device_count` did not count the copies.

## Real-World Use Case
This structure matched how real smart home platforms are organized. Every device shares a common interface (name, room, power), and each type of device inherits that and adds its own behavior. The hub reflected a central controller: when one device receives a bad command or goes offline, the controller logs the failure and keeps managing everything else instead of taking the whole house down. The copying demo also matched a real bug. If an app cloned a device's settings with a shallow copy to make a "vacation profile," editing that profile's schedule would silently change the real thermostat's schedule as well.

## Sample Output (excerpt)
```
=== Copy Demonstration ===
original is shallow? False   original is deep? False
original.schedule is shallow.schedule? True
original.schedule is deep.schedule?    False

After changing the original's weekend morning to 74, night to 60, and target to 72:
  original schedule: {'morning': 68, 'night': 60, 'weekend': {'morning': 74, 'night': 66}}
  shallow schedule:  {'morning': 68, 'night': 60, 'weekend': {'morning': 74, 'night': 66}}   <- changed too (shared dict)
  deep schedule:     {'morning': 68, 'night': 64, 'weekend': {'morning': 70, 'night': 66}}   <- unchanged (independent copy)

=== Student Extension: SmartHub Error Handling ===
Sending a batch of commands, some of them bad:
  OK    Desk Lamp.power(True)
  OK    Office Thermostat.power(True)
  OK    Office Thermostat.set_target(68)
  FAIL  Office Thermostat.set_target(120): 120F is outside the safe range 50-90F
  FAIL  Office Thermostat.set_target('warm'): Temperature must be a number, got str
  FAIL  Desk Lamp does not support 'set_target'
  FAIL  no device named 'Garage Door'

3 of 7 commands succeeded, and the hub is still running.
```

## Reflection

Working on this assignment, I learned how Python looks up attributes on an object first and then on its class, and why that makes class variables shared until something assigns to them through an instance. I also got to see shallow and deep copying side by side instead of just reading about them. The biggest challenge was making the copy demo actually prove the difference, so I used identity checks with `is` and changed nested data on the original to show the shallow copy changing with it. While checking the device counter I also found that `copy()` and `deepcopy()` skip `__init__`, so the copies were never counted. Compared to procedural programming, where data and the functions that change it are separate, OOP kept each device's data together with the rules that protect it. Validation like the safe temperature range lived in one place instead of being repeated everywhere a temperature was set. That paid off for maintainability and reuse, since the thermostat reused all of the parent's code and the hub could manage any future device type without changes. The overhead was extra structure up front, but in a growing application it keeps changes small and safe.
