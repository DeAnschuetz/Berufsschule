from typing import cast

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Buildings.OreMine import OreMine
from Model.GameObjects.Buildings.OreUnloadStation import OreUnloadStation
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.MenuElements.HudElements.HudWidgets.OreProgressBar import OreProgressBar
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.Helicopter import Helicopter
from Model.GameObjects.Vehicles.OreTransport import OreTransport

from Services.ConfigService import getConfig


class SideHud(GameObjectContainer):
    """
    A Class representing the Side Heads-Up Display (HUD) in the Game.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer):
            Provides a Container for Game Objects including Layout and Layer Handling.

    Attributes:
        __gamePlayObjects__ (list[ImageGameObject]): List of GamePlay Objects tracked for status display.
        __hudElements__ (list[ImageGameObject]): HUD UI Elements.
        __bigFont__ (int): Font Size used for larger Text Entries.
        __smallFont__ (int): Font Size used for smaller Text Entries.
        __oreToCollect__ (float): Total Ore Goal for Win Condition.
        __xOffset__ (int): X Coordinate Offset for HUD Alignment.
    """
    __gamePlayObjects__: list[ImageGameObject]
    __hudElements__: list[ImageGameObject]
    __bigFont__: int
    __smallFont__: int
    __oreToCollect__: float
    __xOffset__:int

    def __init__(
            self,
            screen: pygame.Surface,
            gameObjects : list[ImageGameObject],
            oreToCollect : float = 800,
            baseLayer : int = 100
    ):
        """
        Initialize the SideHud Object and create its visual Elements.

        Args:
            screen (pygame.Surface): Screen Surface to render to.
            oreToCollect (float): Total Amount of Ore to be Collected.
            gameObjects (list[ImageGameObject]): List of GamePlay Objects (e.g., Vehicles, Buildings).
            baseLayer (int): Drawing Layer used as Base for HUD Elements.
        """
        config = getConfig()
        screenConfig = config.getScreenConfig()
        sideHudConfig = screenConfig.getHudConfig().getSideHudConfig()
        super().__init__(
            screen=screen,
            baseLayer=baseLayer
        )

        screenWidth = screenConfig.getScreenWidth()
        hudWidth: int = sideHudConfig.getWidth()
        gameWidth: int = screenWidth - hudWidth

        # Settings for toggling HUD parts
        self.__bigFont__ = sideHudConfig.getBigFont()
        self.__smallFont__ = sideHudConfig.getSmallFont()
        self.__oreToCollect__ = oreToCollect
        self.__xOffset__ = screenWidth - (hudWidth // 2)
        self.__hudGameObjects__ = []
        self.__hudTextObjects__ = []

        self.__createSideHudElements__(baseLayer, gameObjects, gameWidth, hudWidth, sideHudConfig)

    def update(self):
        """
        Update all HUD Elements with current Game Data from relevant GamePlay Objects.
        """
        helicopter: Helicopter = next(filter(lambda obj: isinstance(obj, Helicopter), self.__gamePlayObjects__), None)
        oreTransport: OreTransport = next(filter(lambda obj: isinstance(obj, OreTransport), self.__gamePlayObjects__),None)
        oreMine: OreMine = next(filter(lambda obj: isinstance(obj, OreMine), self.__gamePlayObjects__), None)
        oreUnloadStation: OreUnloadStation = next(filter(lambda obj: isinstance(obj, OreUnloadStation), self.__gamePlayObjects__), None)

        cast(TextGameObject, self.getGameObjectById("%OreGoalProgressText%")).updateMessage(f"Progress: {oreUnloadStation.getTotalResourceStored():.1f}/{self.__oreToCollect__:.1f} Ore")
        cast(TextGameObject, self.getGameObjectById("%StolenAmountText%")).updateMessage(f"Helicopter Stole {helicopter.getStolenAmount():.1f} Ore")

        cast(TextGameObject, self.getGameObjectById("%HeliStatusText%")).updateMessage(f"Heli Status: {helicopter.getStatus()}")
        cast(TextGameObject, self.getGameObjectById("%HeliStatusText%")).updateMessage(f"Transport Ore: {oreTransport.getLoadedOreAmount():.1f}")
        cast(TextGameObject, self.getGameObjectById("%DeliveredOreText%")).updateMessage(f"Delivered Ore: {oreUnloadStation.getTotalResourceStored():.1f}")
        cast(TextGameObject, self.getGameObjectById("%OreLeftInMineText%")).updateMessage(f"Ore Left in Mine: {oreMine.getTotalResourceStored():.1f}")
        cast(TextGameObject, self.getGameObjectById("%TransporterSpeed%")).updateMessage(f"Transporter Speed: {oreTransport.getSpeed() * 10:.1f} km/h")

        for gameObject in self.getGameObjects():
            gameObject.update()

    def __createSideHudElements__(self, baseLayer, gameObjects, gameWidth, hudWidth, sideHudConfig):
        """
        Create and Add all Static HUD Components including Background, Divider,
        Progress Bar and Status Text Fields.
        """
        hudBackground: pygame.Surface = pygame.Surface((hudWidth, gameWidth))
        hudBackground.fill((50, 50, 50))
        backgroundImage = ImageGameObject(
            screen=self.__screen__,
            xCoordinate=0,
            yCoordinate=0,
            layer=baseLayer,
            collision=True,
            image=hudBackground

        )
        backgroundImage.setTopLeft((gameWidth, 0))
        self.addGameObject(backgroundImage)

        # Draw the background and divider
        dividerImage: pygame.Surface = pygame.Surface((2, gameWidth))
        dividerImage.fill((200, 200, 200))
        dividerImage: ImageGameObject = ImageGameObject(
            screen=self.__screen__,
            xCoordinate=0,
            yCoordinate=0,
            layer=baseLayer + 1,
            collision=True,
            image=dividerImage
        )
        dividerImage.setTopLeft((gameWidth, 0))
        self.addGameObject(dividerImage)
        self.__gamePlayObjects__ = gameObjects
        oreUnloadStation = next(filter(lambda obj: isinstance(obj, OreUnloadStation), gameObjects), None)

        # Progress towards ore goal
        oreProgressBar = OreProgressBar(
            screen=self.__screen__,
            xCoordinate=self.__xOffset__,
            yCoordinate=sideHudConfig.getYOffset(),
            oreUnloadStation=oreUnloadStation,
            oreToCollect=self.__oreToCollect__,
            baseLayer=baseLayer + 10,
        )
        self.addGameObject(oreProgressBar)

        verticalOffset: int = sideHudConfig.getYOffset() + oreProgressBar.getHeight() + sideHudConfig.getSmallTextSeparation()
        textEntries = [
            ("%OreGoalProgressText%", self.__bigFont__, sideHudConfig.getBigTextSeparation()),
            ("%StolenAmountText%", self.__bigFont__, sideHudConfig.getBigTextSeparation()),
            ("%HeliStatusText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%TransportOreText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%DeliveredOreText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%OreLeftInMineText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%TransporterSpeed%", self.__smallFont__, sideHudConfig.getBigTextSeparation())
        ]
        for text, fontSize, offset in textEntries:
            textObj = TextGameObject(
                message="",
                identifier=text,
                xCoordinate=self.__xOffset__,
                yCoordinate=verticalOffset,
                fontSize=fontSize,
                screen=self.__screen__,
                layer=baseLayer + 2
            )
            verticalOffset = verticalOffset + textObj.getHeight() + offset
            self.addGameObject(textObj)