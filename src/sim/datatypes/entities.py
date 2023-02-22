from __future__ import annotations

from typing import Dict, Optional, Type

import attrs

from src.sim.datatypes import SimPos, items


@attrs.define
class Entity:
    """Base class for any "sentient" object in the sim"""

    pos: SimPos
    consumables: Optional[Dict[Type[items.Consumable], items.Consumable]] = None
