from __future__ import annotations

import random
import attrs

from src.sim.datatypes import items
from src.config.sim_conf import sconf

@attrs.define
class AntFood(items.Item):
    value: float

    @classmethod
    def basic_food(cls):
        """Generates a food item with a random value
        between 0 and 1."""
        
        value = random.random() * sconf.max_new_food_value

        # Randomly distribute food around the map.
        init_pos = items.ItemPos(sconf.sim_x * random.random(),
                                 sconf.sim_y * random.random())
        return cls(pos = init_pos, 
                    value = value)
