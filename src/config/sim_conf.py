import attrs


@attrs.define
class SimConf:
    # Initial simulation settings.
    init_num_basic_ants: int = 10
    init_num_basic_food: int = 10

    # Simulation dimensions are not locked
    # To the screen dimensions.
    sim_x: int = 800
    sim_y: int = 600

    # Pheremone Settings
    init_found_food_pheremone_level: float = 0.0
    init_location_pheremone_level: float = 1.0

    # Food Settings
    max_basic_food_supply: float = 1.0
    min_basic_food_supply: float = 0.1


sconf = SimConf()
