from __future__ import annotations
import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import entities
from src.sim.items import pheremones

from src.sim.datatypes import SimPos

@attrs.define
class Ant(entities.Entity):
    ant_pheremones: pheremones.AntPheremones

    @classmethod
    def basic_ant(cls) -> Ant:
        """Creates yer regular old basic ant"""

        # Lets just put the ants in the middle of the screen for now.
        init_pos = entities.SimPos(sconf.sim_x/2, 
                                   sconf.sim_y/2)

        ant_pheremones = pheremones.AntPheremones.for_ant(pos=init_pos)

        return cls(pos = init_pos, ant_pheremones = ant_pheremones)

