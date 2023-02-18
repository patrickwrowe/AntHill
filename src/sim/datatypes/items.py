from __future__ import annotations

import attrs

@attrs.define
class Item:
    """Base class for non-sentient
    collectible items in the sim."""
    
    pos: ItemPos

@attrs.define
class ItemPos:
    x: float
    y: float