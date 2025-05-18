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
    A Class representing the Heads-Up Display (HUD) of the Game Screen.

    Attributes:
        __hudGameObjects__ (list[GameObject]): List of HUD Components displayed on Screen.
    """
    __hudGameObjects__ : list[GameObject]

    def __init__(self, screen: pygame.Surface, oreToCollect: float = 800, gameObjects: list[GameObject] = None, baseLayer: int = 100):
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
        yCoordinate: int = getConfig().getScreenConfig().getHudConfig().getTopHudConfig().getYCoordinate()
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
        self.__hudGameObjects__ = [sideHud, topHud]

    def updateGameObjects(self):
        """
        Update all HUD GameObjects.
        This calls the update method on each HUD component to refresh their display.
        """
        for hudGameObject in self.__hudGameObjects__:
            cast(GameObjectContainer, hudGameObject).updateHudElements()

    def __str__(self) -> str:
        """
        Return a Detailed String Representation of the Hud Instance,
        Including All HUD GameObjects.
        """
        hudObjectsStr = ", ".join(
            [str(obj) for obj in self.__hudGameObjects__]
        )
        return (
            f"{type(self).__name__}("
            f"hudGameObjects=[{hudObjectsStr}])"
        )