import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Buildings.OreUnloadStation import OreUnloadStation
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Services.ConfigService import getConfig


class OreProgressBar(GameObjectContainer):

    __oreUnloadStation__ : OreUnloadStation
    __oreToCollect__ : float
    __barHeight__ : int
    __barMaxWidth__ : int

    def __init__(self, screen: pygame.Surface, oreUnloadStation: OreUnloadStation, baseLayer: int = 500, xCoordinate: int = 0, yCoordinate: int = 0, oreToCollect: float = 0) -> None:
        super().__init__(
            screen=screen,
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer
        )
        progressBarConfig = getConfig().getScreenConfig().getHudConfig().getSideHudConfig().getProgressBarConfig()
        self.__barHeight__ =  progressBarConfig.getHeight()
        self.__barMaxWidth__ = progressBarConfig.getWidth()
        self.__oreUnloadStation__ = oreUnloadStation
        self.__oreToCollect__ = oreToCollect

        progressBarBackground: pygame.Surface = pygame.Surface(size=(self.__barMaxWidth__, self.__barHeight__))
        progressBarBackground.fill((255, 255, 255))
        oreProgressBackground: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            layer=baseLayer,
            image=progressBarBackground,
            identifier="oreProgressBackground"
        )
        super().addGameObject(oreProgressBackground)


        self.updateGameObjects()

    def getHeight(self):
        return self.__barHeight__

    def getWidth(self):
        return self.__barMaxWidth__

    def updateGameObjects(self):
        self.__updateBarWidth__()
        super().drawByLayer()

    def __updateBarWidth__(self):
        super().removeGameObjectById("oreProgressBar")
        progressBarImage = self.__createCurrentBarImage__()
        oreProgressBar: ImageGameObject = ImageGameObject(
            screen=self.__screen__,
            layer=self.getBaseLayer() + 1,
            collision=False,
            image=progressBarImage,
            identifier="oreProgressBar"
        )
        self.__realignBarWithBackground__(oreProgressBar)
        super().addGameObject(oreProgressBar)

    def __createCurrentBarImage__(self):
        currentBarWidth = self.__getCurrentBarWidthEven__()
        progressBarImage: pygame.Surface = pygame.Surface((currentBarWidth, self.__barHeight__))
        progressBarImage.fill((0, 255, 0))
        return progressBarImage

    def __realignBarWithBackground__(self, oreProgressBar):
        oreProgressBackground = next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "oreProgressBackground" and type(obj) is ImageGameObject), None)
        progressBarTopLeft = oreProgressBackground.getTopLeft()
        oreProgressBar.setTopLeft(progressBarTopLeft)

    def __getCurrentBarWidthEven__(self):
        oreProgress = self.__oreUnloadStation__.getTotalResourceStored() / self.__oreToCollect__
        rawWidth: float = self.__barMaxWidth__ * oreProgress
        currentBarWidth: float = round(rawWidth / 2) * 2
        return currentBarWidth