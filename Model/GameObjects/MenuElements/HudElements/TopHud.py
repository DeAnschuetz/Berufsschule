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
    A Class representing the Top HUD Element including Fuel Level and Ore Loading Status.

    Inherits from:
        GameObject (Model.GameObjects.Base.GameObject) representing the Background of the Top HUD.

    Attributes:
        oreTransport (OreTransport): Ore Transport Object this HUD is linked to.
        fuelLevelBar (ImageGameObject): Visual Bar showing current Fuel Level.
    """
    oreTransport : OreTransport
    fuelLevelBar : FuelLevelBar
    loadLevelBar : LoadLevelBar

    def __init__(self, screen: pygame.Surface, oreTransport: OreTransport, yCoordinate: float = 0, baseLayer: int = 100):
        """
        Initialize a TopHud Object.

        Args:
            screen (pygame.Surface): Surface to draw the HUD on.
            oreTransport (OreTransport): The Ore Transport Object to monitor.
            yCoordinate (float): Y-Coordinate for placing the HUD Elements.
        """
        super().__init__(
            screen=screen,
            baseLayer=baseLayer + 1
        )
        self.oreTransport = oreTransport
        self.__fuelLevelBar__ = FuelLevelBar(
            screen=screen,
            oreTransport=oreTransport,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer
        )
        self.__loadLevelBar__ = LoadLevelBar(
            screen=screen,
            oreTransport=oreTransport,
            yCoordinate=yCoordinate + self.__fuelLevelBar__.getHeight() + 10,
            baseLayer = baseLayer
        )
        topHudBackground: pygame.Surface = pygame.Surface((self.__fuelLevelBar__.getWidth() + 20 + yCoordinate, self.__fuelLevelBar__.getHeight() + self.__loadLevelBar__.getHeight() + 30))
        topHudBackground.fill((50, 50, 50))

        screenConfig = getConfig().getScreenConfig()
        gameWidth: int = screenConfig.getScreenWidth() - screenConfig.getHudConfig().getSideHudConfig().getWidth()

        background = ImageGameObject(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=topHudBackground.get_height() / 2,
            image=topHudBackground,
            layer=baseLayer
        )
        super().addGameObject(background)

    def updateHudElements(self):
        """
        Update and Draw all Top HUD Elements.
        """
        super().updateGameObjects()
        super().drawByLayer()
        self.__loadLevelBar__.updateGameObjects()
        self.__fuelLevelBar__.updateGameObjects()
