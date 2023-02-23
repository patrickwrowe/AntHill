from __future__ import annotations

import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, items


@attrs.define
class Pheremone(items.Consumable):
    @classmethod
    def new_pheremone(cls, pos: SimPos, supply: float = 1.0):
        return cls(pos=pos, supply=supply)


@attrs.define
class AntLocationPheremone(Pheremone):
    """ants leave pheremones where they have been."""

    @classmethod
    def new_pheremone(cls, pos: SimPos):
        return super().new_pheremone(
            pos=pos, supply=sconf.init_location_pheremone_level
        )


@attrs.define
class FoundFoodPheremone(Pheremone):
    """Pheremone is resupplied on finding food.

    Ants leave this trail to indicate to other ants
    where food has been found.
    """

    @classmethod
    def new_pheremone(cls, pos: SimPos):
        return super().new_pheremone(
            pos=pos, supply=sconf.init_found_food_pheremone_level
        )
