import pygame
import math

from Model.GameObjects.Config.GameConfigDynamic import GameConfigDynamic


class GameObject:
    __screen__ : pygame.Surface
    __xCoordinate__: float
    __yCoordinate__: float
    __baseLayer__: int
    __identifier__: str

    def __init__(self, screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0, baseLayer: int = 0, identifier: str = "") -> None:
        self.__xCoordinate__ = xCoordinate
        self.__yCoordinate__ = yCoordinate
        self.__screen__ = screen
        self.__baseLayer__ = baseLayer
        self.__identifier__ = identifier

    def getXCoordinate(self) -> float:
        """Return the X-Coordinate."""
        return self.__xCoordinate__

    def setXCoordinate(self, xCoordinate: float) -> None:
        """Set the X-Coordinate."""
        self.__xCoordinate__ = xCoordinate

    def getYCoordinate(self) -> float:
        """Set the Y-Coordinate."""
        return self.__yCoordinate__

    def setYCoordinate(self, yCoordinate: float) -> None:
        """Return the Y-Coordinate."""
        self.__yCoordinate__ = yCoordinate

    def getScreen(self) -> pygame.Surface:
        """Return the Screen Surface."""
        return self.__screen__

    def getBaseLayer(self) -> int:
        """Return the drawing BaseLayer."""
        return self.__baseLayer__

    def getLayer(self) -> int:
        """
        Return the drawing BaseLayer. This function exists to have the function work with all GameObjects.
        """
        return self.getBaseLayer()

    def setLayer(self, layer: int) -> None:
        """
        Set the drawing BaseLayer. This function exists to have the function work with all GameObjects.
        """
        self.setBaseLayer(layer)

    def setBaseLayer(self, layer: int) -> None:
        """Set the drawing BaseLayer."""
        self.__baseLayer__ = layer

    def getIdentifier(self) -> str:
        """Return the Identifier String of the GameObject."""
        return self.__identifier__

    def setIdentifier(self, identifier: str) -> None:
        """Set the Identifier String of the GameObject."""
        self.__identifier__ = identifier

    def draw(self) -> None:
        """Draw Method to be overridden by Subclasses if needed."""
        pass

    def update(self) -> None:
        """Update Method to be overridden by Subclasses if needed."""
        pass

    def updateGameObjects(self):
        """Update Method to be overridden by Subclasses if needed."""
        pass

    def drawByLayer(self) -> None:
        """Draw Method to be overridden by Subclasses if needed."""
        pass