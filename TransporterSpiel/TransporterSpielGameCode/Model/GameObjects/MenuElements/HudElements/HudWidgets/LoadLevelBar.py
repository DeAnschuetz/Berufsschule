import pygame
from typing import cast

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Services.ConfigService import getConfig

class LoadLevelBar(GameObjectContainer):
    """
    A Class Representing a Load Level Bar for an Ore Transport Vehicle.

    Inherits from:
        GameObjectContainer: Container for GameObjects composing the Load Level Bar.

    Attributes:
        __oreTransport__ (OreTransport): The Ore Transport whose Load Level is monitored.
        __barMaxWidth__ (int): The Maximum Width of the Load Level Bar.
        __barHeight__ (int): The Height of the Load Level Bar.
    """
    __oreTransport__: OreTransport
    __barMaxWidth__: int
    __barHeight__: int

    def __init__(self, screen: pygame.Surface, oreTransport: OreTransport, yCoordinate: float = 40, baseLayer: int = 500):
        """
        Initialize a LoadLevelBar Object with Background and Load Text.

        Args:
            screen (pygame.Surface): Surface to draw the Load Level Bar on.
            oreTransport (OreTransport): The Ore Transport to monitor.
            yCoordinate (float): Y-Coordinate for positioning the Bar.
            baseLayer (int): Base Layer for rendering order.
        """
        config = getConfig()
        screenConfig = config.getScreenConfig()
        loadBarConfig = config.getScreenConfig().getHudConfig().getTopHudConfig().getFuelBarConfig()
        sideHudConfig = screenConfig.getHudConfig().getSideHudConfig()

        gameWidth: int = screenConfig.getScreenWidth() - sideHudConfig.getWidth()

        self.__barMaxWidth__ = loadBarConfig.getWidth()
        self.__barHeight__ = loadBarConfig.getHeight()

        super().__init__(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer + 1
        )

        # Create a white background surface for the load bar
        loadBarBackground: pygame.Surface = pygame.Surface((self.__barMaxWidth__, self.__barHeight__))
        loadBarBackground.fill((255, 255, 255))
        loadBarBackgroundObj: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            layer=self.getBaseLayer(),
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
            layer=self.getBaseLayer() + 2,
            identifier="loadLevelText",
            color=(0, 0, 0)
        )
        self.addGameObject(loadLevelText)
        self.update()

    def update(self):
        """
        Update the Load Level Bar's Visual Width and Text based on Ore Transport's Current Load.
        Removes the old Load Level Bar image and creates a new one reflecting current load percent.
        """
        loadPercent = self.__getLoadPercentRounded__()
        self.__updateBarText__(loadPercent)
        self.removeGameObjectById("loadLevelBar")

        self.__updateBarWidth__()

    def __updateBarWidth__(self):
        """
        Create and add the current Load Level Bar Image reflecting the current load width,
        and realign it with the Load Level Bar Background.
        """
        barImage = self.__createCurrentBarImage__()
        barObject = ImageGameObject(
            screen=self.__screen__,
            image=barImage,
            layer=self.getBaseLayer() + 1,
            identifier="loadLevelBar"
        )
        self.__realignBarWithBackground__(barObject)
        self.addGameObject(barObject)

    def __createCurrentBarImage__(self):
        """
        Create a Surface representing the current load bar width, filled with orange color.

        Returns:
            pygame.Surface: The Surface with the current Load Level Bar width.
        """
        currentBarWidth = self.__getCurrentBarWidthEven__()
        barImage = pygame.Surface((currentBarWidth, self.__barHeight__))
        # Orange color representing Load Level
        barImage.fill((255, 165, 0))
        return barImage


    def __realignBarWithBackground__(self, barObject):
        """
        Align the top-left corner of the Load Level Bar Image with the Load Level Background Image.

        Args:
            barObject (ImageGameObject): The Load Level Bar Image object to align.
        """
        background = cast(ImageGameObject , next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "loadLevelBackground"), None))
        barObject.setTopLeft(background.getTopLeft())

    def __updateBarText__(self, loadPercent):
        """
        Update the Load Level Text to display the current load percentage.

        Args:
            loadPercent (float): Current load percentage as a float between 0 and 1.
        """
        textObject: TextGameObject = cast(TextGameObject, next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "loadLevelText"), None))
        textObject.updateMessage(f"{int(loadPercent * 100)}% Load")

    def __getCurrentBarWidthEven__(self):
        """
        Calculate the current Load Bar width rounded to an even number for consistent rendering.

        Returns:
            int: The current width of the Load Level Bar (even number).
        """
        percent = self.__getLoadPercentRounded__()
        rawWidth = self.__barMaxWidth__ * percent
        # Round width to nearest even number for visual consistency
        return round(rawWidth / 2) * 2

    def __getLoadPercentRounded__(self) -> float:
        """
        Calculate the current Load Bar width rounded to an even number for consistent rendering.

        Returns:
            int: The current width of the Load Level Bar (even number).
        """
        maxLoad = self.__oreTransport__.getOreCapacity()
        currentLoad = self.__oreTransport__.getLoadedOreAmount()
        return round(currentLoad / maxLoad, 2) if maxLoad > 0 else 0.0

    def getHeight(self):
        return self.__barHeight__

    def getWidth(self):
        return self.__barMaxWidth__