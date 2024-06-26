import pytest

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos
from src.sim.entities import ant
from src.sim.items.pheremones import AntLocationPheremone, FoundFoodPheremone, Pheremone
from tests import test_utils


def test_basic_ants():
    new_ant = ant.Ant.basic_ant()
    assert test_utils.check_in_sim_box(new_ant.pos.x, new_ant.pos.y)

    # Get the position of the location pheremone "item"
    old_pheremone_pos = (
        new_ant.consumables[AntLocationPheremone].pos.x,
        new_ant.consumables[AntLocationPheremone].pos.y,
    )
    old_ant_pos = (new_ant.pos.x, new_ant.pos.y)
    assert old_ant_pos == old_pheremone_pos

    # okay now lets move that ant
    new_ant.pos.x += 10
    new_ant.pos.y += 10
    new_ant_pos = (new_ant.pos.x, new_ant.pos.y)
    new_pheremone_pos = (
        new_ant.consumables[AntLocationPheremone].pos.x,
        new_ant.consumables[AntLocationPheremone].pos.y,
    )
    assert new_ant_pos != old_ant_pos
    assert new_ant_pos != old_pheremone_pos

    # Verify that the item contained by the ant moves with the ant.
    # Of course we can just check the identity of these things
    # rather than specific values
    assert new_ant_pos == new_pheremone_pos
    assert new_ant.pos == new_ant.consumables[AntLocationPheremone].pos
    assert new_ant.pos == new_ant.consumables[FoundFoodPheremone].pos


def test_ant_pheremones():
    new_ant = ant.Ant.basic_ant()

    # Check pheremone levels
    assert (
        new_ant.consumables[AntLocationPheremone].location.supply
        == sconf.init_location_pheremone_level
    )
    assert (
        new_ant.consumables[FoundFoodPheremone].supply
        == sconf.init_found_food_pheremone_level
    )

    # test withdrawal of ant_pheremones
    withdrawn = new_ant.consumables[AntLocationPheremone].withdraw(0.5)
    assert new_ant.consumables[AntLocationPheremone].supply == 0.5
    assert withdrawn == 0.5
    withdrawn = new_ant.consumables[AntLocationPheremone].withdraw(0.1)
    assert new_ant.consumables[AntLocationPheremone].supply == 0.4
    assert withdrawn == 0.1

    with pytest.raises(ValueError):
        new_ant.consumables[AntLocationPheremone].supply -= 0.5

    # We should just get what's left over
    withdrawn = new_ant.consumables[AntLocationPheremone].withdraw(0.5)
    assert withdrawn == 0.4

    # should be nothing to withdraw from the found food
    withdrawn = new_ant.consumables[FoundFoodPheremone].withdraw(0.5)
    assert withdrawn == 0.0

    new_ant.consumables[FoundFoodPheremone].deposit(0.5)
    assert new_ant.consumables[FoundFoodPheremone].supply == 0.5


def test_pheremone():
    pos = SimPos(0, 0)
    pheremone = Pheremone(pos=pos, supply=5.0)
    assert pheremone.pos == pos
    assert pheremone.supply == 5.0


def test_ant_location_pheremone():
    pos = SimPos(0, 0)
    pheremone = AntLocationPheremone(pos=pos, supply=10.0)
    assert pheremone.pos == pos
    assert pheremone.supply == 10.0


def test_found_food_pheremone():
    pos = SimPos(0, 0)
    pheremone = FoundFoodPheremone(
        pos=pos, supply=sconf.init_found_food_pheremone_level
    )
    assert pheremone.pos == pos
    assert pheremone.supply == sconf.init_found_food_pheremone_level


def test_ant_pheremones():
    new_ant = ant.Ant.basic_ant()

    # Test that the Ant's pheremones start at the initial levels
    assert (
        new_ant.consumables[AntLocationPheremone].supply
        == sconf.init_location_pheremone_level
    )
    assert (
        new_ant.consumables[FoundFoodPheremone].supply
        == sconf.init_found_food_pheremone_level
    )

    # Test that withdrawing from the Ant's pheremones correctly updates their supply
    initial_location_supply = new_ant.consumables[AntLocationPheremone].supply
    amount_withdrawn = 0.5
    new_ant.consumables[AntLocationPheremone].withdraw(amount_withdrawn)
    assert (
        new_ant.consumables[AntLocationPheremone].supply
        == initial_location_supply - amount_withdrawn
    )

    # Test that depositing into the Ant's pheremones correctly updates their supply
    initial_food_supply = new_ant.consumables[FoundFoodPheremone].supply
    amount_deposited = 0.25
    new_ant.consumables[FoundFoodPheremone].deposit(amount_deposited)
    assert (
        new_ant.consumables[FoundFoodPheremone].supply
        == initial_food_supply + amount_deposited
    )
