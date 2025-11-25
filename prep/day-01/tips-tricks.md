# Tips & Tricks

## Define & decompose
1. Define the problem. Write it down as clearly and specificallly as possible of what the actual computation is
2. Decompose. Break it down into intermediate steps.
2. Apply step 1-2 for each step until most atomic steps possible.

## sets

fast containment checks

## dataclasses

- frozen=True <- dataclass immutable, can become set member/dict key
- use when writing a class that doesn't have a lot of regular methods, but defining a bunch of dunders
- use Field when defining a default value. use default-factory when defining a mutable default value

## cache

- `from functools import cache`, decorator
- lru_cache <- least recently used
  - has a maximum size
  - when reached, the oldest member is evicted
  - used for long-running processes to cache doesn't grow without bounds, otherwise cache is fine
- use when function is called many times with repeated times

## grids (arrays)

-2D grid is a list of lists
