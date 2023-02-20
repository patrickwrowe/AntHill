from __future__ import annotations

import attrs
import numpy as np

from src.config.sim_conf import sconf
from src.sim.datatypes import items, maps


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