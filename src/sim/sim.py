from __future__ import annotations

from typing import Dict, List, Type

import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import entities, items, maps
from src.sim.entities import ant
from src.sim.items import food, pheremones
from src.sim.maps import consumables_maps, environment_maps, meta_map
from src.sim.rules import stochastic


@attrs.define
class AntHillSim:
    """Main class for handling anthill simulation"""

    sim_entities: List[entities.Entity]
    sim_items: List[items.Item]
    sim_maps: Dict[Type[maps.MapArray], maps.MapArray]
    meta_maps: Dict[str, maps.MapArray]
    num_updates: int = 0

    @classmethod
    def new_sim(cls):
        """Initialise a new simulation"""
        raise NotImplementedError()

    def update_sim(self) -> AntHillSim:
        """Update the simulation"""
        raise NotImplementedError()


@attrs.define
class BasicAntHillSim(AntHillSim):
    @classmethod
    def new_sim(cls):
        """Initialise a new simulation"""

        sim_entities = []
        sim_items = []
        sim_maps = {}

        # Initialise some ants.
        sim_entities.extend(
            [ant.Ant.basic_ant() for i in range(sconf.init_num_basic_ants)]
        )
        # Initialise some food
        sim_items.extend(
            [food.BasicAntFood.new_food() for i in range(sconf.init_num_basic_food)]
        )

        # Initialise some maps
        sim_maps[
            pheremones.FoundFoodPheremone
        ] = consumables_maps.ConsumableMap.new_map(
            consumable=pheremones.FoundFoodPheremone
        )
        sim_maps[
            pheremones.AntLocationPheremone
        ] = consumables_maps.ConsumableMap.new_map(
            consumable=pheremones.AntLocationPheremone
        )
        sim_maps[
            environment_maps.TemperatureMap
        ] = environment_maps.TemperatureMap.new_map()
        sim_maps[environment_maps.AltitudeMap] = environment_maps.AltitudeMap.new_map()

        meta_maps = {
            "AltitudeAntLocation": meta_map.MetaMap.new_map(
                sub_maps=[
                    sim_maps[environment_maps.AltitudeMap],
                    sim_maps[pheremones.AntLocationPheremone],
                ],
                coefficients=(1, 1),
            ),
            "AltitudeFoundFood": meta_map.MetaMap.new_map(
                sub_maps=[
                    sim_maps[environment_maps.AltitudeMap],
                    sim_maps[pheremones.FoundFoodPheremone],
                ],
                coefficients=(1, 1),
            ),
        }

        return cls(
            sim_entities=sim_entities,
            sim_items=sim_items,
            sim_maps=sim_maps,
            meta_maps=meta_maps,
        )

    def update_sim(self) -> BasicAntHillSim:
        """Update the simulation"""

        self.num_updates += 1

        if self.num_updates % sconf.recompose_submaps_every == 0:
            for mapname, sim_map in self.meta_maps.items():
                sim_map.recompose_submaps()

        if self.num_updates % sconf.withdraw_pheremones_every == 0:
            self.sim_maps[pheremones.AntLocationPheremone].withdraw_from_entities(
                self.sim_entities, value=sconf.pheremone_withdraw_quant
            )
            self.sim_maps[pheremones.FoundFoodPheremone].withdraw_from_entities(
                self.sim_entities, value=sconf.pheremone_withdraw_quant
            )

        if sconf.brownian_motion == True:
            stochastic.brownian_motion(self.sim_entities)
        if sconf.mmc_move == True:
            stochastic.metropolis_monte_carlo(
                self.sim_entities, self.meta_maps["AltitudeAntLocation"]
            )

        return self
