from __future__ import annotations

import attrs
import numpy as np

from src.config.sim_conf import sconf
from src.sim.datatypes import items, maps, entities

from typing import List

@attrs.define
class ConsumableMap(maps.MapArray):
    consumable: items.Consumable

    @classmethod
    def new_map(cls, consumable: items.Consumable) -> ConsumableMap:
        # By default, a new map is produced with zero values
        # for each index.
        values = np.zeros(
            (sconf.default_map_resolution_x, sconf.default_map_resolution_y)
        )

        return cls(consumable=consumable, values=values)

    def withdraw_from_entities(self, withdraw_entities: List[entities.Entity], value: float) -> np.ndarray:
        """
        Withdraws a quantity 'value' from the type(self.consumable) of every
        entity with type(self.consumable) in its attributes. 
        """

        withdrawn = []
        positions = []

        # first withdraw the correct amount from each entity
        for entity in withdraw_entities:
            withdrawn.append(entity.consumables[type(self.consumable)].withdraw(value))
            positions.append(entity.pos.coords)

        positions = np.array(positions)
        withdrawn = np.array(withdrawn)

        # get a histogram, accounting for the fact that some entities
        # may return nothing when we withdraw from them.
        withdrawn_map, _, _ = np.histogram2d(x = positions[:, 0],
                                       y = positions[:, 1],
                                       range = [[0, self.values.shape[0]],
                                                [0, self.values.shape[1]]],
                                       bins = self.values.shape,
                                       weights = withdrawn)
        
        # Update the new map values with the withdrawn quantity
        self.values += withdrawn_map

        return withdrawn_map
        



