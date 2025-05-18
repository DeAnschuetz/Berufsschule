import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject


class TextGameObject(ImageGameObject):

    __text__: str
    __font__: pygame.font.Font
    __color__: tuple
    __backgroundRect__: pygame.Rect
    __waitForInput__: bool

    def __init__(self, screen: pygame.Surface, message: str, identifier: str = "", xCoordinate: float = 0, yCoordinate: float = 0, fontSize : int = 20, color: tuple = (255, 255, 255), layer: int = 100) -> None:
        self.__font__ = pygame.font.SysFont(None, fontSize)
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
        if color is None:
            color = self.__color__
        textSurface = self.__font__.render(message, True, color)
        super().setImage(textSurface)