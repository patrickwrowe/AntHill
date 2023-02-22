from __future__ import annotations

import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, entities, items
from src.sim.items import pheremones, food

from typing import List, Dict, Type

@attrs.define
class Ant(entities.Entity):

    consumables: Dict[Type[items.Consumable], items.Consumable]

    @classmethod
    def basic_ant(cls) -> Ant:
        """Creates yer regular old basic ant"""

        # Lets just put the ants in the middle of the screen for now.
        init_pos = entities.SimPos(sconf.sim_x / 2, sconf.sim_y / 2)

        init_consumables = {pheremones.AntLocationPheremone: pheremones.AntLocationPheremone.new_pheremone(pos=init_pos),
                            pheremones.FoundFoodPheremone: pheremones.FoundFoodPheremone.new_pheremone(pos=init_pos)}

        return cls(pos=init_pos, consumables=init_consumables)
