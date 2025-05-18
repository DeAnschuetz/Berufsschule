from typing import cast

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Services.ConfigService import getConfig


class FuelLevelBar(GameObjectContainer):
    __oreTransport__: OreTransport
    __barMaxWidth__: int
    __barHeight__: int

    def __init__(self, screen: pygame.Surface, oreTransport: OreTransport, yCoordinate: float = 0, baseLayer: int = 100):
        config = getConfig()
        screenConfig = config.getScreenConfig()
        fuelBarConfig = config.getScreenConfig().getHudConfig().getTopHudConfig().getFuelBarConfig()
        sideHudConfig = screenConfig.getHudConfig().getSideHudConfig()

        gameWidth: int = screenConfig.getScreenWidth() - sideHudConfig.getWidth()

        self.__barMaxWidth__ = fuelBarConfig.getWidth()
        self.__barHeight__ = fuelBarConfig.getHeight()

        fuelBarBackground : pygame.Surface = pygame.Surface((self.__barMaxWidth__, fuelBarConfig.getHeight()))
        fuelBarBackground.fill((255, 255, 255))
        super().__init__(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer + 1,
        )
        fuelBarBackground: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            layer=super().getBaseLayer(),
            image=fuelBarBackground,
            identifier="fuelLevelBackground"
        )
        self.addGameObject(fuelBarBackground)

        self.__oreTransport__ = oreTransport

        fontSize = fuelBarConfig.getFontSize()
        fuelLevelText: TextGameObject = TextGameObject(
            message=f"FUEL%",
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            fontSize=fontSize,
            screen=self.__screen__,
            layer=super().getBaseLayer() + 2,
            identifier="fuelLevelText",
            color=(0, 0 ,0),
        )
        self.addGameObject(fuelLevelText)
        self.updateGameObjects()

    def getHeight(self):
        return self.__barHeight__

    def getWidth(self):
        return self.__barMaxWidth__

    def updateGameObjects(self):
        fuelPercent = self.__getFuelPercentRounded__()
        self.__updateBarText__(fuelPercent)
        super().removeGameObjectById("%fuelLevelBar%")

        self.__updateBarWidth__()

        self.drawByLayer()

    def __updateBarWidth__(self):
        fuelLevelBarImage = self.__createCurrentBarImage__()
        fuelLevelBar: ImageGameObject = ImageGameObject(
            screen=self.__screen__,
            image=fuelLevelBarImage,
            layer=super().getBaseLayer() + 1,
            identifier="%fuelLevelBar%"
        )
        self.__realignBarWithBackground__(fuelLevelBar)
        self.addGameObject(fuelLevelBar)

    def __createCurrentBarImage__(self):
        currentBarWidth = self.__getCurrentBarWidthEven__()
        fuelLevelBarImage: pygame.Surface = pygame.Surface((currentBarWidth, self.__barHeight__))
        fuelLevelBarImage.fill((0, 150, 255))
        return fuelLevelBarImage

    def __realignBarWithBackground__(self, fuelLevelBar: ImageGameObject):
        fuelLevelBackground: ImageGameObject = cast(ImageGameObject, next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "fuelLevelBackground"), None))
        fuelLevelBar.setTopLeft(fuelLevelBackground.getTopLeft())

    def __updateBarText__(self, fuelPercent):
        fuelLevelText: TextGameObject = cast(TextGameObject, next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "fuelLevelText" and type(obj) is TextGameObject), None))
        fuelLevelText.updateMessage(f"{int(fuelPercent * 100)}% Fuel")

    def __getCurrentBarWidthEven__(self):
        fuelPercent = self.__getFuelPercentRounded__()
        rawWidth: float = self.__barMaxWidth__ * fuelPercent
        currentBarWidth: float = round(rawWidth / 2) * 2
        return currentBarWidth

    def __getFuelPercentRounded__(self) -> float:
        maxFuel = self.__oreTransport__.getFuelCapacity()
        currentFuel = self.__oreTransport__.getFuelLevel()
        return round(currentFuel / maxFuel, 2) if maxFuel > 0 else 0.0