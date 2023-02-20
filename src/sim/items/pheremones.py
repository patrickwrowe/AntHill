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

    ...


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


@attrs.define
class AntPheremones:
    pos: SimPos
    location: AntLocationPheremone
    found_food: FoundFoodPheremone

    @classmethod
    def for_ant(cls, pos: SimPos):
        location = AntLocationPheremone.new_pheremone(pos=pos)
        found_food = FoundFoodPheremone.new_pheremone(pos=pos)

        return cls(pos=pos, location=location, found_food=found_food)
