import json


def to_camel_case(snake_str):
    """Convert snake_case or lowerCamelCase to UpperCamelCase."""
    parts = snake_str.split('_') if '_' in snake_str else [snake_str[0].lower() + snake_str[1:]]
    return ''.join(p.capitalize() if i != 0 else p for i, p in enumerate(parts))


class DynamicConfig:
    """
    A class that wraps a dictionary and allows attribute-style access
    and auto-generates getter methods for each attribute.
    """
    def __init__(self, config_dict: dict):
        for key, value in config_dict.items():
            # Recursively wrap dictionaries as DynamicConfig instances
            if isinstance(value, dict):
                value = DynamicConfig(value)
            setattr(self, key, value)

            # Create and attach a getter method on the instance
            camel_method = f"get{key[0].upper()}{key[1:]}"

            # Define the function separately to bind the current key
            def make_getter(k):
                return lambda self=self: getattr(self, k)

            # Bind the generated getter function to this instance
            object.__setattr__(self, camel_method, make_getter(key))

    def __repr__(self):
        return f"<DynamicConfig {self.__dict__}>"

    def get(self, key, default=None):
        """
        Retrieve attribute by key with optional default value.
        """
        return getattr(self, key, default)



class GameConfigDynamic:
    """
    Game-specific Configuration Loader supporting screen size switching
    and dynamic attribute generation based on input configuration.
    """
    def __init__(self, configDict: dict, useSmallScreen: bool = False):
        self.useSmallScreen = useSmallScreen

        # Basic config options with default values
        self.fps = configDict.get("fps", 60)
        self.difficultySelection = configDict.get("difficultySelection", True)

        # Named config sections with predefined getter lambdas
        self.errorMessageConfig = configDict.get("errorMessageConfig", {})
        self.getErrorMessageConfig = lambda: self.errorMessageConfig

        self.finalMessageConfig = configDict.get("finalMessageConfig", {})
        self.getFinalMessageConfig = lambda: self.finalMessageConfig

        self.gameConfig = configDict.get("gameConfig", {})
        self.getGameConfig = lambda: self.gameConfig

        # Generate camelCase getters for basic fields
        self.getFPS = lambda: self.fps
        self.getDifficultySelection = lambda: self.difficultySelection

        # Determine screen config section based on mode
        screenKey = "smallScreenConfig" if useSmallScreen else "bigScreenConfig"
        screenConfig = configDict.get(screenKey, {})

        # Wrap screen config in DynamicConfig for nested attribute access
        self.screen = DynamicConfig(screenConfig)
        self.getScreenConfig = lambda: self.screen

        # Keys to skip from dynamic generation (already handled above)
        excluded_keys = {"fps", "difficultySelection", "smallScreenConfig", "bigScreenConfig"}

        # Dynamically generate attributes and camelCase getters for remaining config sections
        for key, value in configDict.items():
            if key not in excluded_keys:
                attr_value = DynamicConfig(value) if isinstance(value, dict) else value
                setattr(self, key, attr_value)

                # Create a dynamic camelCase getter for each additional section
                camel_method = f"get{to_camel_case(key[0].upper() + key[1:])}"
                setattr(self, camel_method, lambda k=key: getattr(self, k))

    def setSmallScreen(self, useSmall: bool):
        self.useSmallScreen = useSmall

    def __repr__(self):
        mode = "SmallScreenConfig" if self.useSmallScreen else "BigScreenConfig"
        return f"<GameConfigDynamic {mode}: FPS={self.fps}, DifficultySelection={self.difficultySelection}>"

    @staticmethod
    def loadConfigFromFile(path: str = "config.json", useSmallScreen: bool = False) -> "GameConfigDynamic":
        with open(path, "r") as f:
            data = json.load(f)
            return GameConfigDynamic(data, useSmallScreen)
