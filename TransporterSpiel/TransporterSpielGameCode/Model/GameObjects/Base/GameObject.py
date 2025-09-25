import pygame

class GameObject:
    """
    A Class representing the Base Object for all Game Elements.

    This Class provides common Attributes and Methods for all Game Objects,
    such as Position, Drawing Layer, Identifier, and the Drawing Surface.

    Attributes:
        __screen__ (pygame.Surface): The Surface on which the Object is drawn.
        __xCoordinate__ (float): The X-Coordinate of the Object.
        __yCoordinate__ (float): The Y-Coordinate of the Object.
        __baseLayer__ (int): The Drawing Layer of the Object.
        __identifier__ (str): A String Identifier for this Object.
    """
    __screen__ : pygame.Surface
    __xCoordinate__: float
    __yCoordinate__: float
    __baseLayer__: int
    __identifier__: str

    def __init__(self, screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0, baseLayer: int = 0, identifier: str = "") -> None:
        """
        Initialize a GameObject Instance.

        Args:
            screen (pygame.Surface): The Surface this Object will be drawn on.
            xCoordinate (float): Initial X-Coordinate of the Object.
            yCoordinate (float): Initial Y-Coordinate of the Object.
            baseLayer (int): Drawing Layer of the Object.
            identifier (str): Optional Identifier for the Object.
        """
        self.__xCoordinate__ = xCoordinate
        self.__yCoordinate__ = yCoordinate
        self.__screen__ = screen
        self.__baseLayer__ = baseLayer
        self.__identifier__ = identifier

    def draw(self) -> None:
        """
        Draw this Object to the Screen.

        To be overridden by Subclasses with specific Drawing Logic.
        """
        pass

    def update(self) -> None:
        """
        Update the Object's State.

        To be overridden by Subclasses to implement Game Logic.
        """
        pass

    def getXCoordinate(self) -> float:
        return self.__xCoordinate__

    def setXCoordinate(self, xCoordinate: float) -> None:
        self.__xCoordinate__ = xCoordinate

    def getYCoordinate(self) -> float:
        return self.__yCoordinate__

    def setYCoordinate(self, yCoordinate: float) -> None:
        self.__yCoordinate__ = yCoordinate

    def getScreen(self) -> pygame.Surface:
        return self.__screen__

    def getBaseLayer(self) -> int:
        return self.__baseLayer__

    def getLayer(self) -> int:
        """
        Return the drawing BaseLayer. This function exists to have the function work with all GameObjects.
        """
        return self.getBaseLayer()

    def setLayer(self, layer: int) -> None:
        """
        Set the Drawing Layer for this Object.

        This Function is intended for Uniform Layer Handling across Objects.
        """
        self.setBaseLayer(layer)

    def setBaseLayer(self, layer: int) -> None:
        self.__baseLayer__ = layer

    def getIdentifier(self) -> str:
        return self.__identifier__

    def setIdentifier(self, identifier: str) -> None:
        self.__identifier__ = identifier

    def __str__(self) -> str:
        """
        Return a detailed String Representation of this GameObject Instance.
        """
        return (
            f"{type(self).__name__} (xCoordinate={self.getXCoordinate}, yCoordinate={self.getYCoordinate}, "
            f"layer={self.getBaseLayer}, identifier='{self.getIdentifier}', screen=<{type(self.getScreen).__name__}>)"
        )
