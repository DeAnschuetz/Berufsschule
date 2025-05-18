from typing import cast

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Buildings.OreMine import OreMine
from Model.GameObjects.Buildings.OreUnloadStation import OreUnloadStation
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.MenuElements.HudElements.HudWidgets.OreProgressBar import OreProgressBar
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.Helicopter import Helicopter
from Model.GameObjects.Vehicles.OreTransport import OreTransport

from Services.ConfigService import getConfig


class SideHud(GameObject):
    __gamePlayObjects__: list[ImageGameObject]
    __hudElements__: list[ImageGameObject]
    __oreProgressBar__: OreProgressBar
    __bigFont__: int
    __smallFont__: int
    __oreToCollect__: float
    __xOffset__:int

    def __init__(self, screen: pygame.Surface, oreToCollect : float = 800, gameObjects : list[ImageGameObject] = None, baseLayer : int = 100):
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

    def __createSideHudElements__(self, baseLayer, gameObjects, gameWidth, hudWidth, sideHudConfig):
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
        self.__gamePlayObjects__ = gameObjects
        oreUnloadStation = next(filter(lambda obj: isinstance(obj, OreUnloadStation), gameObjects), None)
        # Progress towards ore goal
        self.__oreProgressBar__ = OreProgressBar(
            screen=self.__screen__,
            xCoordinate=self.__xOffset__,
            yCoordinate=sideHudConfig.getYOffset(),
            oreUnloadStation=oreUnloadStation,
            oreToCollect=self.__oreToCollect__,
            baseLayer=baseLayer + 10,
        )
        verticalOffset: int = sideHudConfig.getYOffset() + self.__oreProgressBar__.getHeight() + sideHudConfig.getSmallTextSeparation()
        self.__hudElements__ =  ([dividerImage, backgroundImage])
        textEntries = [
            ("%OreGoalProgressText%", self.__bigFont__, sideHudConfig.getBigTextSeparation()),
            ("%StolenAmountText%", self.__bigFont__, sideHudConfig.getBigTextSeparation()),
            ("%HeliStatusText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%TransportOreText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%DeliveredOreText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation()),
            ("%OreLeftInMineText%", self.__smallFont__, sideHudConfig.getSmallTextSeparation())
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
            self.__hudElements__.append(textObj)

    def getHudElementById(self, identifier: str):
        return next((obj for obj in self.__hudElements__ if obj.getIdentifier() == identifier), None)

    def updateHudElements(self):
        """Update all HUD Elements with the latest Game State Information."""
        helicopter: Helicopter = next(filter(lambda obj: isinstance(obj, Helicopter), self.__gamePlayObjects__), None)
        oreTransport: OreTransport = next(filter(lambda obj: isinstance(obj, OreTransport), self.__gamePlayObjects__), None)
        oreMine: OreMine = next(filter(lambda obj: isinstance(obj, OreMine), self.__gamePlayObjects__), None)
        oreUnloadStation: OreUnloadStation = next(filter(lambda obj: isinstance(obj, OreUnloadStation), self.__gamePlayObjects__), None)

        cast(TextGameObject, self.getHudElementById("%OreGoalProgressText%")).updateMessage(f"Progress: {oreUnloadStation.getTotalResourceStored():.1f}/{self.__oreToCollect__:.1f} Ore")
        cast(TextGameObject, self.getHudElementById("%StolenAmountText%")).updateMessage(f"Helicopter Stole {helicopter.getStolenAmount():.1f} Ore")

        cast(TextGameObject, self.getHudElementById("%HeliStatusText%")).updateMessage(f"Heli Status: {helicopter.getStatus()}")
        cast(TextGameObject, self.getHudElementById("%HeliStatusText%")).updateMessage(f"Transport Ore: {oreTransport.getLoadedOreAmount():.1f}")
        cast(TextGameObject, self.getHudElementById("%DeliveredOreText%")).updateMessage(f"Delivered Ore: {oreUnloadStation.getTotalResourceStored():.1f}")
        cast(TextGameObject, self.getHudElementById("%OreLeftInMineText%")).updateMessage(f"Ore Left in Mine: {oreMine.getTotalResourceStored():.1f}")

        self.__hudElements__.sort(key=lambda obj: obj.getLayer())
        for gameObject in self.__hudElements__:
            gameObject.draw()
        self.__oreProgressBar__.updateGameObjects()
