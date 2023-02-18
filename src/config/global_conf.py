import attrs

@attrs.define
class GlobalConfig:

    scrn_ht: int = 600
    scrn_wdt: int = 800
    headless: bool = True

gconf = GlobalConfig()