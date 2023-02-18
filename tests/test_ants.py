import pytest

from src.config.sim_conf import sconf
from src.sim.entities import ant
from tests import test_utils


def test_basic_ants():
    new_ant = ant.Ant.basic_ant()
    assert test_utils.check_in_sim_box(new_ant.pos.x, new_ant.pos.y)

    # Get the position of the location pheremone "item"
    old_pheremone_pos = (
        new_ant.ant_pheremones.location.pos.x,
        new_ant.ant_pheremones.location.pos.y,
    )
    old_ant_pos = (new_ant.pos.x, new_ant.pos.y)
    assert old_ant_pos == old_pheremone_pos

    # okay now lets move that ant
    new_ant.pos.x += 10
    new_ant.pos.y += 10
    new_ant_pos = (new_ant.pos.x, new_ant.pos.y)
    new_pheremone_pos = (
        new_ant.ant_pheremones.location.pos.x,
        new_ant.ant_pheremones.location.pos.y,
    )
    assert new_ant_pos != old_ant_pos
    assert new_ant_pos != old_pheremone_pos

    # Verify that the item contained by the ant moves with the ant.
    # Of course we can just check the identity of these things
    # rather than specific values
    assert new_ant_pos == new_pheremone_pos
    assert new_ant.pos == new_ant.ant_pheremones.location.pos
    assert new_ant.pos == new_ant.ant_pheremones.found_food.pos


def test_ant_pheremones():
    new_ant = ant.Ant.basic_ant()

    # Check pheremone levels
    assert new_ant.ant_pheremones.location.supply == sconf.init_location_pheremone_level
    assert (
        new_ant.ant_pheremones.found_food.supply
        == sconf.init_found_food_pheremone_level
    )

    # test withdrawal of ant_pheremones
    withdrawn = new_ant.ant_pheremones.location.withdraw(0.5)
    assert new_ant.ant_pheremones.location.supply == 0.5
    assert withdrawn == 0.5
    withdrawn = new_ant.ant_pheremones.location.withdraw(0.1)
    assert new_ant.ant_pheremones.location.supply == 0.4
    assert withdrawn == 0.1

    with pytest.raises(ValueError):
        new_ant.ant_pheremones.location.supply -= 0.5

    # We should just get what's left over
    withdrawn = new_ant.ant_pheremones.location.withdraw(0.5)
    assert withdrawn == 0.4

    # should be nothing to withdraw from the found food
    withdrawn = new_ant.ant_pheremones.found_food.withdraw(0.5)
    assert withdrawn == 0.0

    new_ant.ant_pheremones.found_food.deposit(0.5)
    assert new_ant.ant_pheremones.found_food.supply == 0.5
