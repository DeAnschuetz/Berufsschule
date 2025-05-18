import json


def to_camel_case(snake_str):
    """Convert snake_case or lowerCamelCase to UpperCamelCase."""
    parts = snake_str.split('_') if '_' in snake_str else [snake_str[0].lower() + snake_str[1:]]
    return ''.join(p.capitalize() if i != 0 else p for i, p in enumerate(parts))


class DynamicConfig:
    def __init__(self, config_dict: dict):
        for key, value in config_dict.items():
            if isinstance(value, dict):
                value = DynamicConfig(value)
            setattr(self, key, value)

            # Create and attach a getter method on the instance
            camel_method = f"get{key[0].upper()}{key[1:]}"
            # Define the function separately to bind the current key
            def make_getter(k):
                return lambda self=self: getattr(self, k)
            # Bind to the instance as method name
            object.__setattr__(self, camel_method, make_getter(key))

    def __repr__(self):
        return f"<DynamicConfig {self.__dict__}>"

    def get(self, key, default=None):
        return getattr(self, key, default)



class GameConfigDynamic:
    def __init__(self, config_dict: dict, useSmallScreen: bool = False):
        self.useSmallScreen = useSmallScreen
        self.fps = config_dict.get("fps", 60)
        self.difficultySelection = config_dict.get("difficultySelection", True)

        self.errorMessageConfig = config_dict.get("errorMessageConfig", {})
        self.getErrorMessageConfig = lambda: self.errorMessageConfig

        self.gameConfig = config_dict.get("gameConfig", {})
        self.getGameConfig = lambda: self.gameConfig

        # Create camelCase getters
        self.getFPS = lambda: self.fps
        self.getDifficultySelection = lambda: self.difficultySelection

        # Load screen config
        screenKey = "smallScreenConfig" if useSmallScreen else "bigScreenConfig"
        screenConfig = config_dict.get(screenKey, {})
        self.screen = DynamicConfig(screenConfig)
        self.getScreenConfig = lambda: self.screen

        # Load other configs dynamically (excluding screen configs)
        excluded_keys = {"fps", "difficultySelection", "smallScreenConfig", "bigScreenConfig"}
        for key, value in config_dict.items():
            if key not in excluded_keys:
                attr_value = DynamicConfig(value) if isinstance(value, dict) else value
                setattr(self, key, attr_value)

                # Create camelCase getter dynamically
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
