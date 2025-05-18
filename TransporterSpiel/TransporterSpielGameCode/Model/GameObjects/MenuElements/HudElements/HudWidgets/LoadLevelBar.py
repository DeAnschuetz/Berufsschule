import pygame
from typing import cast

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Services.ConfigService import getConfig


class LoadLevelBar(GameObjectContainer):
    __oreTransport__: OreTransport
    __barMaxWidth__: int
    __barHeight__: int

    def __init__(self, screen: pygame.Surface, oreTransport: OreTransport, yCoordinate: float = 40, baseLayer: int = 500):
        config = getConfig()
        screenConfig = config.getScreenConfig()
        loadBarConfig = config.getScreenConfig().getHudConfig().getTopHudConfig().getFuelBarConfig()
        sideHudConfig = screenConfig.getHudConfig().getSideHudConfig()

        gameWidth: int = screenConfig.getScreenWidth() - sideHudConfig.getWidth()

        self.__barMaxWidth__ = loadBarConfig.getWidth()
        self.__barHeight__ = loadBarConfig.getHeight()

        loadBarBackground: pygame.Surface = pygame.Surface((self.__barMaxWidth__, self.__barHeight__))
        loadBarBackground.fill((255, 255, 255))

        super().__init__(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer + 1
        )

        loadBarBackgroundObj: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            layer=super().getBaseLayer(),
            image=loadBarBackground,
            identifier="loadLevelBackground"
        )
        self.addGameObject(loadBarBackgroundObj)

        self.__oreTransport__ = oreTransport

        fontSize = loadBarConfig.getFontSize()
        loadLevelText = TextGameObject(
            message="LOAD%",
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            fontSize=fontSize,
            screen=self.__screen__,
            layer=super().getBaseLayer() + 2,
            identifier="loadLevelText",
            color=(0, 0, 0)
        )
        self.addGameObject(loadLevelText)
        self.updateGameObjects()

    def getHeight(self):
        return self.__barHeight__

    def getWidth(self):
        return self.__barMaxWidth__

    def updateGameObjects(self):
        loadPercent = self.__getLoadPercentRounded__()
        self.__updateBarText__(loadPercent)
        super().removeGameObjectById("loadLevelBar")

        self.__updateBarWidth__()

        self.drawByLayer()

    def __updateBarWidth__(self):
        barImage = self.__createCurrentBarImage__()
        barObject = ImageGameObject(
            screen=self.__screen__,
            image=barImage,
            layer=super().getBaseLayer() + 1,
            identifier="loadLevelBar"
        )
        self.__realignBarWithBackground__(barObject)
        self.addGameObject(barObject)

    def __createCurrentBarImage__(self):
        currentBarWidth = self.__getCurrentBarWidthEven__()
        barImage = pygame.Surface((currentBarWidth, self.__barHeight__))
        barImage.fill((255, 165, 0))  # Orange for load level
        return barImage

    def __realignBarWithBackground__(self, barObject):
        background = next((obj for obj in self.getGameObjects()
                           if obj.getIdentifier() == "loadLevelBackground"), None)
        barObject.setTopLeft(background.getTopLeft())

    def __updateBarText__(self, loadPercent):
        textObject: TextGameObject = cast(TextGameObject, next((obj for obj in self.getGameObjects()
                                                                if obj.getIdentifier() == "loadLevelText"), None))
        textObject.updateMessage(f"{int(loadPercent * 100)}% Load")

    def __getCurrentBarWidthEven__(self):
        percent = self.__getLoadPercentRounded__()
        rawWidth = self.__barMaxWidth__ * percent
        return round(rawWidth / 2) * 2

    def __getLoadPercentRounded__(self) -> float:
        maxLoad = self.__oreTransport__.getOreCapacity()
        currentLoad = self.__oreTransport__.getLoadedOreAmount()
        return round(currentLoad / maxLoad, 2) if maxLoad > 0 else 0.0
