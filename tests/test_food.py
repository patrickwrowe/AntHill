from src.sim.items import food
from src.config.sim_conf import sconf
from tests import test_utils
import pytest
import numpy as np

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
    assert np.isclose(new_food.supply,  0.4 / norm_fact)
    assert np.isclose(withdrawn, 0.1 / norm_fact)
    
    with pytest.raises(ValueError):
        new_food.supply -= 0.5 / norm_fact
        print(new_food.supply)
    
    # We should just get what's left over
    withdrawn = new_food.withdraw(0.5 / norm_fact)
    assert np.isclose(withdrawn, 0.4 / norm_fact)
