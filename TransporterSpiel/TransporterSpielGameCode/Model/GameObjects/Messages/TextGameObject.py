import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject


class TextGameObject(ImageGameObject):
    """
    A Class Representing a Text Game Object rendered on the screen using Pygame.

    Inherits From:
        ImageGameObject: Base Class that handles Image Rendering and Positioning.

    Attributes:
        __text__ (str): The Current Text Message displayed.
        __font__ (pygame.font.Font): The Font used to Render the Text.
        __color__ (tuple): RGB Color of the Text.
        __backgroundRect__ (pygame.Rect): Optional Background Rectangle (not used here).
        __waitForInput__ (bool): Flag for Waiting for User Input (not used here).
    """

    __text__: str
    __font__: pygame.font.Font
    __color__: tuple
    __backgroundRect__: pygame.Rect
    __waitForInput__: bool

    def __init__(self, screen: pygame.Surface, message: str, identifier: str = "", xCoordinate: float = 0, yCoordinate: float = 0, fontSize : int = 20, color: tuple = (255, 255, 255), layer: int = 100) -> None:
        """
        Initialize a TextGameObject with given parameters.

        Args:
            screen (pygame.Surface): The Surface to Render the Text on.
            message (str): The Initial Text Message to Display.
            identifier (str): Optional Identifier for the Object.
            xCoordinate (float): X Position of the Text Object.
            yCoordinate (float): Y Position of the Text Object.
            fontSize (int): Size of the Font to Render the Text.
            color (tuple): RGB Color Tuple for the Text.
            layer (int): Drawing Layer for Rendering Order.
        """
        self.__font__ = pygame.font.SysFont(None, fontSize)
        # Render initial text surface using the font and color
        textSurface = self.__font__.render(message, True, color)
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=False,
            image=textSurface,
            layer=layer,
            screen=screen,
            identifier=identifier
        )
        self.__text__ = message
        self.__color__ = color


    def updateMessage(self, message: str, color: tuple = None) -> None:
        """
        Update the Displayed Text Message and optionally the Text Color.

        Args:
            message (str): New Text Message to Render.
            color (tuple, optional): RGB Color Tuple to use for Rendering.
                Defaults to the previously used text color.

        Notes:
            Re-renders the Text Surface and updates the Image in the superclass.
        """
        if color is None:
            color = self.__color__
        textSurface = self.__font__.render(message, True, color)
        super().setImage(textSurface)

    def __str__(self) -> str:
        """
        Return a Detailed String Representation of the TextGameObject,
        Including Current Text, Color, Font Size, Position, Layer, and Screen Info.

        Returns:
            str: String representation of the object state.
        """
        return (
            f"{type(self).__name__}("
            f"text='{self.__text__}', "
            f"color={self.__color__}, "
            f"fontSize={self.__font__.get_height()}, "
            f"xCoordinate={self.getXCoordinate()}, "
            f"yCoordinate={self.getYCoordinate()}, "
            f"collision={self.getCollision()}, "
            f"layer={self.getLayer()}, "
            f"screen=<{type(self.getScreen()).__name__}>, "
            f"identifier='{self.getIdentifier()}')"
        )