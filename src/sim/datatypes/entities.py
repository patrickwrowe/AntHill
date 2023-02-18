from __future__ import annotations
import attrs

@attrs.define
class Entity:
    """Base class for any "sentient" object in the sim"""
    pos: EntityPos
    

@attrs.define
class EntityPos:
    x: float
    y: float