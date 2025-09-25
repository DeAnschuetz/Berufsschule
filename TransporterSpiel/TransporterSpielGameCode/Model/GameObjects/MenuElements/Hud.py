from typing import cast

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.MenuElements.HudElements.SideHud import SideHud
from Model.GameObjects.MenuElements.HudElements.TopHud import TopHud
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Services.ConfigService import getConfig


class Hud(GameObjectContainer):
    """
    A Class representing the Heads-Up Display (HUD) in the Game.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer): Base Class for Grouping GameObjects.
    """

    def __init__(self, screen: pygame.Surface, oreToCollect: float = 800, gameObjects: list[GameObject] = None, baseLayer: int = 100):
        """
        Initialize a Hud Object with Side and Top HUD Elements.

        Args:
            screen (pygame.Surface): Surface to draw the HUD on.
            oreToCollect (float): Amount of Ore to Collect for Completion.
            gameObjects (list[GameObject]): List of GameObjects in the Game.
            baseLayer (int): Base Layer used for rendering.
        """
        """
        Initialize a Hud Object with Side and Top HUD Elements.

        Args:
            screen (pygame.Surface): Surface to draw the HUD on.
            oreToCollect (float): Amount of Ore to Collect for Completion.
            gameObjects (list[ImageGameObject]): List of GameObjects in the Game.
        """
        super().__init__(
            screen=screen,
            baseLayer=baseLayer
        )

        # Get configured Y-Coordinate for Top HUD placement
        yCoordinate: int = getConfig().getScreenConfig().getHudConfig().getTopHudConfig().getYCoordinate()

        # Find the OreTransport instance among the GameObjects (if any)
        oreTransport = next(filter(lambda obj: isinstance(obj, OreTransport), gameObjects), None)
        topHud: TopHud = TopHud(
            screen=screen,
            oreTransport=oreTransport,
            yCoordinate=yCoordinate,
            baseLayer= super().getBaseLayer() + 1
        )
        sideHud: SideHud= SideHud(
            screen=screen,
            oreToCollect=oreToCollect,
            gameObjects=gameObjects,
            baseLayer= super().getBaseLayer() + 1
        )
        self.__gameObjects__ = [sideHud, topHud]

    def __updateGameObjects__(self):
        """
        Update all HUD GameObjects.

        This calls the update and draw methods on each HUD component
        to refresh their visual representation.
        """
        for hudGameObject in self.__gameObjects__:
            hudGameObject.update()
            hudGameObject.draw()

    def __str__(self) -> str:
        """
        Return a detailed String Representation of the Hud Instance,
        including references to internal HUD elements.
        """
        return (
            f"{type(self).__name__} (baseLayer={self.getBaseLayer()}, "
            f"screen=<{type(self.getScreen()).__name__}>, "
            f"gameObjects={[type(obj).__name__ for obj in self.__gameObjects__]})"
        )