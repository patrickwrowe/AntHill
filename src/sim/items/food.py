from __future__ import annotations

import numpy as np
import attrs

from src.sim.datatypes import items
from src.config.sim_conf import sconf

@attrs.define
class Food(items.Item):
    supply: float = attrs.field(validator=attrs.validators.ge(0.0))

    @classmethod
    def new_food(cls):
        raise NotImplementedError

    def withdraw_food(self, quant):
        """Food has a finite supply"""
        # If there's nothing to withdraw, do nothing
        if self.supply == 0.0:
            return 0.0
        # If there's only a small amount left,
        # Withdraw what can be withdrawn
        elif quant > self.supply:
            residal = self.supply
            self.supply = 0.0
            return residal
        # Else, withdraw everything
        else:
            self.supply -= quant
            return quant
    
    def add_food(self, quant):
        self.supply += quant

@attrs.define
class BasicAntFood(Food):
    @classmethod
    def new_food(cls):
        """Generates a food item with a random value
        between 0 and 1."""
        
        # Basic food takes a random value between the min
        # and max parameters.
        supply = np.random.uniform(sconf.min_basic_food_supply, 
                                   sconf.max_basic_food_supply)

        # Randomly distribute food around the map.
        init_pos = items.ItemPos(sconf.sim_x * np.random.uniform(),
                                 sconf.sim_y * np.random.uniform())

        return cls(pos = init_pos, 
                   supply = supply)