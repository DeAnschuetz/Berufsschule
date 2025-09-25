import time
from typing import cast

import pygame
from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject


class TimedTextGameObject(GameObjectContainer):
    """
    A Container Class for displaying a Timed Text Message with a Background on the Screen.

    The Text and Background fade out smoothly over a given Duration after creation.

    Attributes:
        __startTime__ (float): Timestamp when the Object was created.
        __duration__ (float): Time in Seconds the Message is displayed before it expires.
    """
    __startTime__ : time.time
    __duration__ : float

    def __init__(
            self,
            message: str,
            xCoordinate: float,
            yCoordinate: float,
            fontSize : int,
            screen: pygame.Surface,
            color: tuple = (255, 255, 255),
            backgroundColor: tuple = (70, 70, 70),
            borderSize: int = 20,
            layer : int = 15,
            duration: float = 2.0
    ):
        """
        Initialize a TimedTextGameObject with Text and Background Images.

        Args:
            message (str): The Text Message to display.
            xCoordinate (float): X position on the screen.
            yCoordinate (float): Y position on the screen.
            fontSize (int): Font size of the text.
            screen (pygame.Surface): Surface to render the message on.
            color (tuple, optional): RGB Color of the text. Defaults to white (255, 255, 255).
            backgroundColor (tuple, optional): RGB Color of the background rectangle. Defaults to dark gray (70, 70, 70).
            borderSize (int, optional): Padding around the text for background size. Defaults to 20.
            layer (int, optional): Base drawing layer. Defaults to 15.
            duration (float, optional): How long to display the message in seconds. Defaults to 2.0.
        """
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            screen=screen,
            baseLayer=layer,
        )

        # Create the TextGameObject with slightly higher layer than background
        temporaryText: TextGameObject = TextGameObject(
            message=message,
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            fontSize=fontSize,
            screen=screen,
            color=color,
            layer= super().getBaseLayer() + 1,
            identifier="%text%"
        )
        self.addGameObject(temporaryText)

        # Calculate background size with border padding
        backgroundWidth: int = temporaryText.getWidth() + borderSize
        backgroundHeight: int = temporaryText.getHeight() + borderSize
        backgroundImage: pygame.Surface = pygame.Surface((backgroundWidth, backgroundHeight))
        backgroundImage.fill(backgroundColor)
        background= ImageGameObject(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            screen=screen,
            layer= self.getBaseLayer(),
            image=backgroundImage,
            identifier="%background%"
        )
        self.__startTime__ = time.time()
        self.__duration__ = duration


        self.addGameObject(background)

    def draw(self) -> None:
        """
        Update the transparency (alpha) of the Text and Background based on elapsed Time,
        fading them out smoothly from mostly opaque to almost transparent over the duration.
        """
        # Calculate how much time has passed
        elapsed = time.time() - self.__startTime__
        ratio = min(elapsed / self.__duration__, 1.0)

        # Compute alpha: from 10 to 180
        startAlpha = 180
        endAlpha = 10
        currentAlpha = int(startAlpha + (endAlpha - startAlpha) * ratio)

        # Set the current alpha on the background image
        cast(ImageGameObject, self.getGameObjectById("%background%")).setAlpha(currentAlpha)
        cast(ImageGameObject, self.getGameObjectById("%text%")).setAlpha(currentAlpha + 20)
        super().draw()

    def isExpired(self) -> bool:
        """
        Check whether the Message display time has passed its Duration.

        Returns:
            bool: True if expired, False otherwise.
        """
        return time.time() - self.__startTime__ > self.__duration__