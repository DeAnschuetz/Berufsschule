from typing import cast

import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Buildings.OreUnloadStation import OreUnloadStation
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Services.ConfigService import getConfig

class OreProgressBar(GameObjectContainer):
    """
    A Class representing a Progress Bar displaying how much Ore has been collected
    at an OreUnloadStation.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer): Container for related HUD objects.

    Attributes:
        __oreUnloadStation__ (OreUnloadStation): Station from which Ore Collection Progress is retrieved.
        __oreToCollect__ (float): The Target Amount of Ore to collect.
        __barHeight__ (int): Height of the Progress Bar.
        __barMaxWidth__ (int): Maximum Width of the Progress Bar when full.
    """
    __oreUnloadStation__ : OreUnloadStation
    __oreToCollect__ : float
    __barHeight__ : int
    __barMaxWidth__ : int

    def __init__(
            self,
            screen: pygame.Surface,
            oreUnloadStation: OreUnloadStation,
            baseLayer: int = 500,
            xCoordinate: int = 0,
            yCoordinate: int = 0,
            oreToCollect: float = 0
    ) -> None:
        """
        Initialize an OreProgressBar Object.

        Args:
            screen (pygame.Surface): Surface to draw the Progress Bar on.
            oreUnloadStation (OreUnloadStation): Unload Station to monitor.
            baseLayer (int): Rendering Layer of the Bar.
            xCoordinate (int): X-Coordinate for positioning the Bar.
            yCoordinate (int): Y-Coordinate for positioning the Bar.
            oreToCollect (float): Total Ore required to fill the bar completely.
        """
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

        # Create static background for progress bar
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
        self.addGameObject(oreProgressBackground)
        self.update()

    def update(self):
        """
        Update the Load Level Bar's Visual Width and Text based on Ore Transport's Current Load.
        Removes the old Load Level Bar image and creates a new one reflecting current load percent.
        """
        self.removeGameObjectById("oreProgressBar")

        self.__updateBarWidth__()

    def __updateBarWidth__(self):
        """
        Internal Helper that removes the old Bar and adds a newly sized one based on progress.
        """
        self.removeGameObjectById("oreProgressBar")
        progressBarImage = self.__createCurrentBarImage__()
        oreProgressBar: ImageGameObject = ImageGameObject(
            screen=self.__screen__,
            layer=self.getBaseLayer() + 1,
            collision=False,
            image=progressBarImage,
            identifier="oreProgressBar"
        )
        self.__realignBarWithBackground__(oreProgressBar)
        self.addGameObject(oreProgressBar)

    def __createCurrentBarImage__(self):
        """
        Create a Green Bar Surface representing the Current Ore Collection Progress.

        Returns:
            pygame.Surface: Progress Bar Image based on current Ore Level.
        """
        currentBarWidth = self.__getCurrentBarWidthEven__()
        progressBarImage: pygame.Surface = pygame.Surface((currentBarWidth, self.__barHeight__))
        progressBarImage.fill((0, 255, 0))
        return progressBarImage

    def __realignBarWithBackground__(self, oreProgressBar):
        """
        Align the newly created Ore Progress Bar with the Background Bar.
        """
        oreProgressBackground = next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "oreProgressBackground" and type(obj) is ImageGameObject), None)
        progressBarTopLeft = cast(ImageGameObject, oreProgressBackground).getTopLeft()
        oreProgressBar.setTopLeft(progressBarTopLeft)

    def __getCurrentBarWidthEven__(self):
        """
        Calculate the Width of the Progress Bar based on Current Ore Stored.

        Ensures the width is always even to avoid visual jitter.

        Returns:
            int: Even Width for the Progress Bar.
        """
        oreProgress = self.__oreUnloadStation__.getTotalResourceStored() / self.__oreToCollect__
        rawWidth: float = self.__barMaxWidth__ * oreProgress
        currentBarWidth: float = round(rawWidth / 2) * 2
        return currentBarWidth

    def getHeight(self):
        return self.__barHeight__

    def getWidth(self):
        return self.__barMaxWidth__