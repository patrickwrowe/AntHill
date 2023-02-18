from src.sim.entities import ant
from tests import test_utils

def test_basic_ants():
    new_ant = ant.Ant.basic_ant()
    assert test_utils.check_in_sim_box(new_ant.pos.x, new_ant.pos.y)
    assert new_ant.pheremones.location_pheremone == 1.0


