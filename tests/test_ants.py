import pytest
from src.sim.entities import ant
from src.config.sim_conf import sconf
from tests import test_utils
import attrs

def test_basic_ants():
    new_ant = ant.Ant.basic_ant()
    assert test_utils.check_in_sim_box(new_ant.pos.x, new_ant.pos.y)
    

def test_ant_pheremones():

    new_ant = ant.Ant.basic_ant()

    # Check pheremone levels
    assert new_ant.ant_pheremones.location.supply == sconf.init_location_pheremone_level
    assert new_ant.ant_pheremones.found_food.supply == sconf.init_found_food_pheremone_level

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