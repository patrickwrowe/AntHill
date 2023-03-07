from __future__ import annotations

from typing import Dict, List, Optional, Type

import attrs
import numpy as np

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, items


@attrs.define
class Entity:
    """Base class for any "sentient" object in the sim"""

    pos: SimPos
    consumables: Optional[Dict[Type[items.Consumable], items.Consumable]] = None

    def withdraw_from_consumables(
        self,
        consumables: List[items.Consumable],
        value: float = sconf.item_withdraw_quant,
        min_dist: float = sconf.item_collect_dist,
    ) -> None:
        """
        When provided with a list of consumables, withdraw a fixed amount from those
        which are close enough.

        Args:
            consumables: a list of consumables to withdraw from.
            value: quantity to withdraw from each item.
            min_dist: minimum distance from entity to item in order to withdraw.
        Returns:
            None
        """

        # can we speed this up? We could provide the threshold in units of distance**2
        # And then only compute the square of the distance maybe?
        consumables_positions = np.array(
            [consumable.pos.coords for consumable in consumables]
        )
        boolean_distances = (
            np.linalg.norm(self.pos.coords - consumables_positions, axis=1) < min_dist
        )

        for to_widthdraw, consumable in zip(boolean_distances, consumables):
            if not to_widthdraw:
                continue
            else:
                # withdraw a set amount to the correct type of consumable
                quant = consumable.withdraw(value)
                self.consumables[type(consumable)].deposit(quant)
