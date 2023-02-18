from src.config.sim_conf import sconf


def check_in_sim_box(x, y):
    if not 0 < x < sconf.sim_x:
        return False
    if not 0 < y < sconf.sim_y:
        return False
    else:
        return True
