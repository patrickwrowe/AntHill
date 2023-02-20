from __future__ import annotations

import attrs

from src.sim.datatypes import SimPos

@attrs.define
class Entity:
    """Base class for any "sentient" object in the sim"""

    pos: SimPos
