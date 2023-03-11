from __future__ import annotations

import attrs
import numpy as np

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, items


@attrs.define
class Food(items.Consumable):

    @classmethod
    def new_food(cls):
        raise NotImplementedError


@attrs.define
class BasicAntFood(Food):

    @classmethod
    def new_food(cls):
        """Generates a food item with a random value
        between 0 and 1."""

        # Basic food takes a random value between the min
        # and max parameters.
        supply = np.random.uniform(
            sconf.min_basic_food_supply, sconf.max_basic_food_supply
        )

        # Randomly distribute food around the map.
        init_pos = SimPos(
            sconf.sim_x * np.random.uniform(), sconf.sim_y * np.random.uniform()
        )

        return cls(pos=init_pos, supply=supply)
    