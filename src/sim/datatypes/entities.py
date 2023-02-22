from __future__ import annotations

import attrs

from src.sim.datatypes import SimPos, items
from typing import Dict, Type, Optional

@attrs.define
class Entity:
    """Base class for any "sentient" object in the sim"""

    pos: SimPos
    consumables: Optional[Dict[Type[items.Consumable], items.Consumable]] = None
