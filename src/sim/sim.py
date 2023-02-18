from typing import List

import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import entities, items
from src.sim.entities import ant
from src.sim.items import food
from src.sim.rules import stochastic

@attrs.define
class AntHillSim:
    """Main class for handling anthill simulation"""

    sim_entities: List[entities.Entity]
    sim_items: List[items.Item]
    num_updates: int = 0

    @classmethod
    def new_sim(cls):
        """Initialise a new simulation"""
        raise NotImplementedError()

    def update_sim(self) -> List[entities.Entity]:
        """Update the simulation"""
        raise NotImplementedError()


@attrs.define
class BasicAntHillSim(AntHillSim):
    @classmethod
    def new_sim(cls):
        """Initialise a new simulation"""

        sim_entities = []
        sim_items = []

        # Initialise some ants.
        sim_entities.extend(
            [ant.Ant.basic_ant() for i in range(sconf.init_num_basic_ants)]
        )
        # Initialise some food
        sim_items.extend(
            [food.BasicAntFood.new_food() for i in range(sconf.init_num_basic_food)]
        )

        return cls(sim_entities=sim_entities, sim_items=sim_items)

    def update_sim(self):
        """Update the simulation"""

        self.num_updates += 1
        stochastic.random_move(self.sim_entities)

        return self.sim_entities