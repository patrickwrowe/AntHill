import attrs

@attrs.define
class SimConf:

    # Initial simulation settings.
    init_num_ants: int = 10
    init_num_food: int = 10
    
    # Simulation dimensions are not locked
    # To the screen dimensions.
    sim_x = 800
    sim_y = 600

sconf = SimConf()