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
        consumables_positions: np.ndarray,
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

    def deposit_to_consumables(
        self,
        consumables: List[items.Consumable],
        consumables_positions: np.ndarray,
        value: float = sconf.item_withdraw_quant,
        min_dist: float = sconf.item_collect_dist,
    ) -> None:
        """
        When provided with a list of consumables, deposits a fixed amount from those
        which are close enough.

        Args:
            consumables: a list of consumables to withdraw from.
            value: quantity to withdraw from each item.
            min_dist: minimum distance from entity to item in order to withdraw.
        Returns:
            None
        """

        boolean_distances = (
            np.linalg.norm(self.pos.coords - consumables_positions, axis=1) < min_dist
        )

        for to_deposit, consumable in zip(boolean_distances, consumables):
            if not to_deposit:
                continue
            else:
                # withdraw a set amount to the correct type of consumable
                quant = self.consumables[type(consumable)].withdraw(value)
                consumable.deposit(quant)

    def has_consumable(self, consumable: Type[items.Consumable]):
        """Returns true of the specific consumable type supply
        is greater than 0."""

        if self.consumables[consumable].supply > 0.0:
            return True
        else:
            return False
