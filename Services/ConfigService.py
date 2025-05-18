from Model.GameObjects.Config.GameConfigDynamic import GameConfigDynamic

CONFIG_INSTANCE = None

def loadConfig(useSmallScreen=False, path="config.json"):
    global CONFIG_INSTANCE
    if CONFIG_INSTANCE is None:
        CONFIG_INSTANCE = GameConfigDynamic.loadConfigFromFile(path, useSmallScreen)
    else:
        raise Exception("Config already loaded")

def getConfig():
    if CONFIG_INSTANCE is None:
        raise Exception("Config not loaded yet. Call load_config() first.")
    return CONFIG_INSTANCE
