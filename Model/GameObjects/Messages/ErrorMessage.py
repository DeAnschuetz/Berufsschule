import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Services.ConfigService import getConfig
from Services.PygameService import waitForKeyPress


class ErrorTextGameObject(GameObjectContainer):

    errorFooter : TextGameObject
    errorMessage: TextGameObject

    def __init__(self, screen: pygame.Surface, message: str, messageFontSize : int = 26, baseLayer: int = -1000):
        config = getConfig()
        errorMessageConfig = config.getErrorMessageConfig()
        footerMessage: str = errorMessageConfig.getFooterMessage()
        footerFontSize: int = errorMessageConfig.getFooterFontSize()
        footerFontColor: list[int] = errorMessageConfig.getFooterFontColor()
        messageFontColor: list[int] = errorMessageConfig.getMessageFontColor()
        super().__init__(
            screen=screen,
            baseLayer=baseLayer
        )
        errorMessage = TextGameObject(
            message=message,
            xCoordinate=screen.get_width() / 2,
            yCoordinate=screen.get_height() / 2,
            fontSize=messageFontSize,
            screen=screen,
            color=(messageFontColor[0], messageFontColor[1], messageFontColor[2]),
            layer=baseLayer
        )
        super().addGameObject(errorMessage)
        errorFooter = TextGameObject(
            message=footerMessage,
            xCoordinate=screen.get_width() / 2,
            yCoordinate=screen.get_height() / 2 + errorMessage.getHeight(),
            fontSize=footerFontSize,
            screen=screen,
            color=(footerFontColor[0], footerFontColor[1], footerFontColor[2]),
            layer=baseLayer
        )
        super().addGameObject(errorFooter)

    def updateGameObjects(self):
        self.__screen__.fill((30, 30, 30))
        super().drawByLayer()

        # the Error Message will handle its own Input and Drawing!
        pygame.display.update()
        waitForKeyPress(pygame.K_RETURN)
