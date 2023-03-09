from __future__ import annotations

from typing import Dict, List, Protocol, Type

import attrs
import numpy as np
from scipy.ndimage.filters import gaussian_filter

from src.config.sim_conf import sconf
from src.sim.datatypes import entities, items, maps
from src.sim.entities import ant
from src.sim.items import food, pheremones
from src.sim.maps import consumables_maps, environment_maps, meta_map
from src.sim.rules import stochastic


@attrs.define
class AntHillSim(Protocol):
    """Main class for handling anthill simulation"""

    sim_entities: List[entities.Entity]
    sim_items: List[items.Item]
    sim_maps: Dict[Type[maps.MapArray], maps.MapArray]
    meta_maps: Dict[str, maps.MapArray]
    num_updates: int

    @classmethod
    def new_sim(cls):
        """Initialise a new simulation"""
        raise NotImplementedError()

    def update_sim(self) -> AntHillSim:
        """Update the simulation"""
        raise NotImplementedError()


@attrs.define
class BasicAntHillSim(AntHillSim):
    entity_lists: Dict[str, List[entities.Entity]]

    @classmethod
    def new_sim(cls):
        """Initialise a new simulation"""

        sim_entities = []
        sim_items = []
        sim_maps = {}
        entity_lists = {}

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
                coefficients=(1, -1),
            ),
            "AltitudeFoundFood": meta_map.MetaMap.new_map(
                sub_maps=[
                    sim_maps[environment_maps.AltitudeMap],
                    sim_maps[pheremones.FoundFoodPheremone],
                ],
                coefficients=(1, -1),
            ),
        }

        entity_lists["ants_with_food"] = [
            entity
            for entity in sim_entities
            if entity.has_consumable(food.BasicAntFood)
        ]
        entity_lists["ants_without_food"] = [
            entity
            for entity in sim_entities
            if not entity.has_consumable(food.BasicAntFood)
        ]

        return cls(
            sim_entities=sim_entities,
            sim_items=sim_items,
            sim_maps=sim_maps,
            meta_maps=meta_maps,
            num_updates=0,
            entity_lists=entity_lists,
        )

    def update_sim(self) -> BasicAntHillSim:
        """Update the simulation, return the current state
        for visualisation."""

        self.num_updates += 1

        # If necessary, update submaps (potential)
        if self.num_updates % sconf.recompose_submaps_every == 0:
            for _, sim_map in self.meta_maps.items():
                sim_map.recompose_submaps()

        # if necessary, withdraw pheremones from ants
        if self.num_updates % sconf.withdraw_pheremones_every == 0:
            self.sim_maps[pheremones.AntLocationPheremone].withdraw_from_entities(
                self.entity_lists["ants_without_food"],
                value=sconf.pheremone_withdraw_quant,
            )
            self.sim_maps[pheremones.FoundFoodPheremone].withdraw_from_entities(
                self.entity_lists["ants_with_food"],
                value=sconf.pheremone_withdraw_quant,
            )

            # Experimental "diffusion"
            # If successful move to consumables map base class
            self.sim_maps[pheremones.AntLocationPheremone].values = gaussian_filter(
                self.sim_maps[pheremones.AntLocationPheremone].values,
                sigma=sconf.pheremone_map_gauss_sigma,
            )
            self.sim_maps[pheremones.FoundFoodPheremone].values = gaussian_filter(
                self.sim_maps[pheremones.FoundFoodPheremone].values,
                sigma=sconf.pheremone_map_gauss_sigma,
            )

        # Withdraw items like food into ants
        if self.num_updates % sconf.withdraw_items_every:
            # can we speed this up? We could provide the threshold in units of distance**2
            # And then only compute the square of the distance maybe?
            consumables_positions = np.array(
                [consumable.pos.coords for consumable in self.sim_items]
            )
            for entity in self.sim_entities:
                entity.withdraw_from_consumables(
                    consumables=self.sim_items,
                    value=sconf.item_withdraw_quant,
                    consumables_positions=consumables_positions,
                )

            # Update Entity Lists, track which ants have food.
            self.entity_lists["ants_with_food"] = [
                entity
                for entity in self.sim_entities
                if entity.has_consumable(food.BasicAntFood)
            ]
            self.entity_lists["ants_without_food"] = [
                entity
                for entity in self.sim_entities
                if not entity.has_consumable(food.BasicAntFood)
            ]

        # move the ants according to some physical laws.
        if sconf.brownian_motion == True:
            stochastic.brownian_motion(self.sim_entities)
        if sconf.mmc_move == True:
            stochastic.metropolis_monte_carlo(
                self.entity_lists["ants_without_food"],
                self.meta_maps["AltitudeFoundFood"],
            )
            stochastic.metropolis_monte_carlo(
                self.entity_lists["ants_with_food"],
                self.meta_maps["AltitudeAntLocation"],
            )

        return self
