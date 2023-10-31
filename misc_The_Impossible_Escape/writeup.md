# srdnlenctf 2023

## The Impossible Escape

It is evident that any attempt to interact with a previously instantiated `TIE()` object will prove ineffective. The cleverest approach involves overriding the `__setattr__()` method of the entire `TIE()` class with, for example, the `print()` function, and subsequently instantiating a new object.

### Solution

Payload: `setattr(TIE,"__setattr__",print);TIE()`