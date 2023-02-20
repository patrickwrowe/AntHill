from src.sim.datatypes import SimPos
from src.sim.datatypes.items import Item, Consumable

def test_item():
    pos = SimPos(0, 0)
    item = Item(pos)
    assert item.pos == pos

def test_consumable():
    pos = SimPos(0, 0)
    consumable = Consumable(pos, supply=10.0)
    assert consumable.pos == pos
    assert consumable.supply == 10.0

def test_withdraw():
    pos = SimPos(0, 0)
    consumable = Consumable(pos, supply=10.0)
    withdrawn = consumable.withdraw(5.0)
    assert withdrawn == 5.0
    assert consumable.supply == 5.0

def test_withdraw_exceed_supply():
    pos = SimPos(0, 0)
    consumable = Consumable(pos, supply=10.0)
    withdrawn = consumable.withdraw(15.0)
    assert withdrawn == 10.0
    assert consumable.supply == 0.0

def test_withdraw_empty_supply():
    pos = SimPos(0, 0)
    consumable = Consumable(pos, supply=0.0)
    withdrawn = consumable.withdraw(5.0)
    assert withdrawn == 0.0
    assert consumable.supply == 0.0

def test_deposit():
    pos = SimPos(0, 0)
    consumable = Consumable(pos, supply=10.0)
    consumable.deposit(5.0)
    assert consumable.supply == 15.0