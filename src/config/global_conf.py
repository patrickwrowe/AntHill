import attrs

@attrs.define
class GlobalConfig:

    scrn_ht: int = 800
    scrn_wdt: int = 600

gconf = GlobalConfig()