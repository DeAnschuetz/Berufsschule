from Model.GameObjects.Config.GameConfigDynamic import GameConfigDynamic

CONFIG_INSTANCE = None

def loadConfig(useSmallScreen=False, path="config.json"):
    """
    Load the Game Configuration from a JSON File.

    Creates a Singleton Configuration Instance by loading the Configuration File.
    Raises an Exception if called more than once.

    Args:
        useSmallScreen (bool): Whether to load Small Screen Settings.
        path (str): Path to the Configuration File.

    Raises:
        Exception: If the Configuration has already been loaded.
    """
    global CONFIG_INSTANCE
    if CONFIG_INSTANCE is None:
        CONFIG_INSTANCE = GameConfigDynamic.loadConfigFromFile(path, useSmallScreen)
    else:
        raise Exception("Config already loaded")

def getConfig():
    """
    Retrieve the Game Configuration Instance.

    Returns the already-loaded Configuration. Raises an Exception if not loaded.

    Returns:
        GameConfigDynamic: The Loaded Configuration Object.

    Raises:
        Exception: If Configuration has not been loaded yet.
    """
    if CONFIG_INSTANCE is None:
        raise Exception("Config not loaded yet. Call load_config() first.")
    return CONFIG_INSTANCE
