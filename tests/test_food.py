import numpy as np
import pytest

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos
from src.sim.items import food
from src.sim.entities import ant
from tests import test_utils


def test_basic_food():
    new_food = food.BasicAntFood.new_food()
    assert sconf.min_basic_food_supply < new_food.supply < sconf.max_basic_food_supply
    assert test_utils.check_in_sim_box(new_food.pos.x, new_food.pos.y)

    # new food has a random value, testing is a little trickier
    norm_fact = sconf.max_basic_food_supply / new_food.supply
    withdrawn = new_food.withdraw(0.5 / norm_fact)
    assert np.isclose(new_food.supply, 0.5 / norm_fact)
    assert np.isclose(withdrawn, 0.5 / norm_fact)
    withdrawn = new_food.withdraw(0.1 / norm_fact)
    assert np.isclose(new_food.supply, 0.4 / norm_fact)
    assert np.isclose(withdrawn, 0.1 / norm_fact)

    with pytest.raises(ValueError):
        new_food.supply -= 0.5 / norm_fact
        print(new_food.supply)

    # We should just get what's left over
    withdrawn = new_food.withdraw(0.5 / norm_fact)
    assert np.isclose(withdrawn, 0.4 / norm_fact)

def test_withdraw_from_food_item():
    new_food = food.BasicAntFood(pos=SimPos(0, 0), supply=2.5)
    new_ant = ant.Ant.basic_ant()

    # ant should not withdraw due to distance
    new_ant.pos = SimPos(10, 10)
    new_ant.withdraw_from_consumables([new_food], value=1.0)
    assert new_food.supply == 2.5
    assert new_ant.consumables[type(new_food)].supply == 0.0

    # closer ant should withdraw.
    # Step 1: withdraw 1.0. Step 2: Withdraw 1.0
    # Step 3: request 1.0, withdraw 0.5 up to limit, leave supply empty
    # Step 4: request 1.0 from empty supply, withdraw 0.
    exp_ant_food_level = [1.0, 2.0, 2.5, 2.5]
    exp_food_supply = [1.5, 0.5, 0.0, 0.0]

    for i in range(4):
        new_ant.pos = SimPos(1, 1)
        new_ant.withdraw_from_consumables([new_food], value=1.0)
        assert new_food.supply == exp_food_supply[i]
        assert new_ant.consumables[type(new_food)].supply == exp_ant_food_level[i]
