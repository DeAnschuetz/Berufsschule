import time

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject


class TimedTextGameObject(GameObjectContainer):

    __startTime__ : time.time
    __duration__ : float
    __temporaryText__: TextGameObject
    __background__: ImageGameObject

    def __init__(self, message: str, xCoordinate: float, yCoordinate: float, fontSize : int, screen: pygame.Surface, color: tuple = (255, 255, 255), backgroundColor: tuple = (70, 70, 70), borderSize: int = 20, layer : int = 15, duration: float = 2.0):
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            screen=screen,
            baseLayer=layer,
        )

        self.__temporaryText__: TextGameObject = TextGameObject(
            message=message,
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            fontSize=fontSize,
            screen=screen,
            color=color,
            layer= super().getBaseLayer() + 1
        )

        backgroundWidth: int =  self.__temporaryText__.getWidth() + borderSize
        backgroundHeight: int =  self.__temporaryText__.getHeight() + borderSize
        backgroundImage: pygame.Surface = pygame.Surface((backgroundWidth, backgroundHeight))
        backgroundImage.fill(backgroundColor)
        self.__background__ = ImageGameObject(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            screen=screen,
            layer= super().getBaseLayer(),
            image=backgroundImage
        )
        self.__startTime__ = time.time()
        self.__duration__ = duration
        if xCoordinate - (self.__background__.getWidth() / 2) - 10 < 0:
            xCoordinate = (self.__background__.getWidth() / 2) + 10
            self.__temporaryText__.setXCoordinate(xCoordinate)
            self.__background__.setXCoordinate(xCoordinate)

    def updateGameObjects(self) -> None:
        # Calculate how much time has passed
        elapsed = time.time() - self.__startTime__
        ratio = min(elapsed / self.__duration__, 1.0)

        # Compute alpha: from 10 to 180
        startAlpha = 180
        endAlpha = 10
        currentAlpha = int(startAlpha + (endAlpha - startAlpha) * ratio)

        # Set the current alpha on the background image
        self.__background__.setAlpha(currentAlpha)
        self.__temporaryText__.setAlpha(currentAlpha + 20)
        self.draw()

    def draw(self) -> None:
        self.__background__.draw()
        self.__temporaryText__.draw()

    def isExpired(self) -> bool:
        return time.time() - self.__startTime__ > self.__duration__
