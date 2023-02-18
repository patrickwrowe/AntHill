from __future__ import annotations
import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import entities

@attrs.define
class Ant(entities.Entity):
    pheremones: AntPheremones

    @classmethod
    def basic_ant(cls) -> Ant:
        """Creates yer regular old basic ant"""
        pheremones = AntPheremones(location_pheremone=1)

        # Lets just put the ants in the middle of the screen for now.
        init_pos = entities.EntityPos(sconf.sim_x/2, 
                                      sconf.sim_y/2)

        return cls(pos = init_pos, pheremones = pheremones)

@attrs.define
class AntPheremones:

    # ants leave pheremones where they have been
    # this is how much of that pheremone the ant has
    location_pheremone: float