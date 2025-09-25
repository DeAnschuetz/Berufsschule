import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.MenuElements.HudElements.HudWidgets.FuelLevelBar import FuelLevelBar
from Model.GameObjects.MenuElements.HudElements.HudWidgets.LoadLevelBar import LoadLevelBar
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Services.ConfigService import getConfig


class TopHud(GameObjectContainer):
    """
    A Class representing the Top Heads-Up Display (HUD) for the Game Screen.

    This HUD contains multiple HUD Elements such as Fuel Level Bar and Load Level Bar,
    positioned near the top of the screen and centered horizontally.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer):
            Container for multiple GameObjects with layering and rendering control.
    """

    def __init__(self, screen: pygame.Surface, oreTransport: OreTransport, yCoordinate: float = 0, baseLayer: int = 100):
        """
        Initialize a TopHud Object with Fuel and Load Level Bars and a Background.

        Args:
            screen (pygame.Surface): Surface to draw the HUD on.
            oreTransport (OreTransport): The Ore Transport Vehicle to monitor HUD values for.
            yCoordinate (float): Vertical offset for placing HUD Elements from the top.
            baseLayer (int): Base layer used for rendering order of HUD Elements.
        """
        super().__init__(
            screen=screen,
            baseLayer=baseLayer + 1
        )
        # Create and add Fuel Level Bar HUD element
        fuelLevelBar = FuelLevelBar(
            screen=screen,
            oreTransport=oreTransport,
            yCoordinate=yCoordinate,
            baseLayer=self.__baseLayer__
        )
        self.addGameObject(fuelLevelBar)

        # Create and add Load Level Bar HUD element, positioned below the Fuel Level Bar with some padding
        loadLevelBar = LoadLevelBar(
            screen=screen,
            oreTransport=oreTransport,
            yCoordinate=yCoordinate + fuelLevelBar.getHeight() + 10,
            baseLayer = self.__baseLayer__
        )
        self.addGameObject(loadLevelBar)

        # Calculate center X position for the background based on screen config (centered horizontally)
        screenConfig = getConfig().getScreenConfig()
        gameWidth: int = screenConfig.getScreenWidth() - screenConfig.getHudConfig().getSideHudConfig().getWidth()

        # Create a semi-transparent background surface sized to encompass both bars and some padding
        topHudBackground: pygame.Surface = pygame.Surface((loadLevelBar.getWidth() + 20 + yCoordinate, fuelLevelBar.getHeight() + loadLevelBar.getHeight() + 30))
        topHudBackground.fill((50, 50, 50))
        # Calculate center x position for the background based on screen config (centered horizontally)
        background = ImageGameObject(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=topHudBackground.get_height() / 2,
            image=topHudBackground,
            layer=baseLayer
        )
        self.addGameObject(background)

    def __str__(self) -> str:
        """
        Return a detailed String Representation of the TopHud instance,
        including its class name and relevant attribute information.
        """
        return (
            f"{type(self).__name__} (baseLayer={self.__baseLayer__}, "
            f"containedGameObjectsCount={len(self.getGameObjects())}, "
            f"screen=<{type(self.getScreen()).__name__}>)"
        )