from src.sim.items import food
from tests import test_utils

def test_basic_food():
    new_food = food.AntFood.basic_food()
    assert 0 < new_food.value < 1
    assert test_utils.check_in_sim_box(new_food.pos.x, new_food.pos.y)
