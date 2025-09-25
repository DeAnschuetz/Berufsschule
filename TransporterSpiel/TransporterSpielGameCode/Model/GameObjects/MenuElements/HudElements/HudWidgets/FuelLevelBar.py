from typing import cast

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Services.ConfigService import getConfig


class FuelLevelBar(GameObjectContainer):
    """
    A Class representing a Fuel Level Bar made up of a Background, a Dynamic Fuel Indicator, and a Text Label.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer) to manage multiple visual elements.

    Attributes:
        __oreTransport__ (OreTransport): The Ore Transport whose Fuel Level is monitored.
        __barMaxWidth__ (int): Maximum Width of the Fuel Indicator Bar.
        __barHeight__ (int): Height of the Fuel Indicator Bar.
    """
    __oreTransport__: OreTransport
    __barMaxWidth__: int
    __barHeight__: int

    def __init__(self, screen: pygame.Surface, oreTransport: OreTransport, yCoordinate: float = 0, baseLayer: int = 100):
        """
        Initialize a FuelLevelBar Object with visual components for background, fuel bar, and fuel text.

        Args:
            screen (pygame.Surface): The Surface to render all elements to.
            oreTransport (OreTransport): The Ore Transport to track.
            yCoordinate (float): The Y-Coordinate for vertical alignment.
            baseLayer (int): The Base Layer to start drawing elements on.
        """
        config = getConfig()
        screenConfig = config.getScreenConfig()
        fuelBarConfig = config.getScreenConfig().getHudConfig().getTopHudConfig().getFuelBarConfig()
        sideHudConfig = screenConfig.getHudConfig().getSideHudConfig()

        gameWidth: int = screenConfig.getScreenWidth() - sideHudConfig.getWidth()

        self.__barMaxWidth__ = fuelBarConfig.getWidth()
        self.__barHeight__ = fuelBarConfig.getHeight()

        super().__init__(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer + 1,
        )

        # Create White Background Surface
        fuelBarBackground : pygame.Surface = pygame.Surface((self.__barMaxWidth__, fuelBarConfig.getHeight()))
        fuelBarBackground.fill((255, 255, 255))
        fuelBarBackground: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            layer=self.getBaseLayer(),
            image=fuelBarBackground,
            identifier="fuelLevelBackground"
        )
        self.addGameObject(fuelBarBackground)

        self.__oreTransport__ = oreTransport

        # Add Static Text Placeholder, Updated Later
        fontSize = fuelBarConfig.getFontSize()
        fuelLevelText: TextGameObject = TextGameObject(
            message=f"FUEL%",
            xCoordinate=gameWidth / 2,
            yCoordinate=yCoordinate,
            fontSize=fontSize,
            screen=self.__screen__,
            layer=self.getBaseLayer() + 2,
            identifier="%fuelLevelText%",
            color=(0, 0 ,0),
        )
        self.addGameObject(fuelLevelText)
        self.update()

    def getHeight(self):
        return self.__barHeight__

    def getWidth(self):
        return self.__barMaxWidth__

    def update(self):
        """
        Update the Fuel Bar and Text Label based on the current Fuel Percentage.
        """
        fuelPercent = self.__getFuelPercentRounded__()
        self.__updateBarText__(fuelPercent)
        self.removeGameObjectById("%fuelLevelBar%")

        self.__updateBarWidth__()

    def __updateBarWidth__(self):
        """
        Create a new Fuel Bar with Width proportional to current Fuel,
        then align and add it to the GameObject Container.
        """
        fuelLevelBarImage = self.__createCurrentBarImage__()
        fuelLevelBar: ImageGameObject = ImageGameObject(
            screen=self.__screen__,
            image=fuelLevelBarImage,
            layer=self.getBaseLayer() + 1,
            identifier="%fuelLevelBar%"
        )
        self.__realignBarWithBackground__(fuelLevelBar)
        self.addGameObject(fuelLevelBar)

    def __createCurrentBarImage__(self):
        """
        Create the colored bar Surface for the current Fuel Level.

        Returns:
            pygame.Surface: A blue rectangle representing current fuel.
        """
        currentBarWidth = self.__getCurrentBarWidthEven__()
        fuelLevelBarImage: pygame.Surface = pygame.Surface((currentBarWidth, self.__barHeight__))
        fuelLevelBarImage.fill((0, 150, 255))
        return fuelLevelBarImage


    def __realignBarWithBackground__(self, fuelLevelBar: ImageGameObject):
        """
        Align the new Fuel Bar Image with the Background for consistent positioning.
        """
        fuelLevelBackground: ImageGameObject = cast(ImageGameObject, next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "fuelLevelBackground"), None))
        fuelLevelBar.setTopLeft(fuelLevelBackground.getTopLeft())

    def __updateBarText__(self, fuelPercent):
        """
        Update the Fuel Text GameObject with the current Fuel Percentage.
        """
        fuelLevelText: TextGameObject = cast(TextGameObject, next((obj for obj in self.getGameObjects() if obj.getIdentifier() == "%fuelLevelText%" and type(obj) is TextGameObject), None))
        fuelLevelText.updateMessage(f"{int(fuelPercent * 100)}% Fuel")

    def __getCurrentBarWidthEven__(self):
        """
        Calculate current Fuel Bar Width, rounding to the next even integer.

        Returns:
            float: Rounded even Width for graphical consistency.
        """
        fuelPercent = self.__getFuelPercentRounded__()
        rawWidth: float = self.__barMaxWidth__ * fuelPercent
        currentBarWidth: float = round(rawWidth / 2) * 2
        return currentBarWidth

    def __getFuelPercentRounded__(self) -> float:
        """
        Safely calculate Fuel Percentage and round to two decimal places.

        Returns:
            float: Fuel Level divided by Capacity, or 0 if Capacity is 0.
        """
        maxFuel = self.__oreTransport__.getFuelCapacity()
        currentFuel = self.__oreTransport__.getFuelLevel()
        return round(currentFuel / maxFuel, 2) if maxFuel > 0 else 0.0