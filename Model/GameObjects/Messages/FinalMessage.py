import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Services.PygameService import waitForKeyPress


class FinalTextGameObject(GameObjectContainer):
    def __init__(self, screen: pygame.Surface, message: str, borderSize: int = 30, messageFontSize: int = 26 , messageFontColor : tuple = (255, 255, 255),  footerMessage : str = "Press ENTER to Continue", footerFontSize : int = 22, footerFontColor : tuple[int, int, int] = (255, 255, 255), backgroudColor: tuple[int, int, int]  = (50, 50, 50)):
        super().__init__(
            screen=screen,
            baseLayer=100000
        )
        finalMessage = TextGameObject(
            message=message,
            xCoordinate=screen.get_width() // 2,
            yCoordinate=screen.get_height() // 2,
            fontSize=messageFontSize,
            screen=screen,
            color=messageFontColor,
            layer=super().getBaseLayer() + 1,
        )
        super().addGameObject(finalMessage)
        footer = TextGameObject(
            message=footerMessage,
            xCoordinate=screen.get_width() // 2,
            yCoordinate=screen.get_height() // 2 + finalMessage.getHeight() + 10,
            fontSize=footerFontSize,
            screen=screen,
            color=footerFontColor,
            layer=super().getBaseLayer() + 1,
        )
        super().addGameObject(footer)
        backgroundWidth = max(finalMessage.getWidth(), footer.getWidth()) + borderSize
        backgroundHeight = finalMessage.getHeight() + footer .getHeight() + 10 + borderSize
        backgroundImageSurface : pygame.Surface = pygame.Surface((backgroundWidth, backgroundHeight))
        backgroundImageSurface.fill(backgroudColor)
        backgroundImage: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=screen.get_width() // 2,
            yCoordinate=screen.get_height() // 2 + 10,
            image=backgroundImageSurface,
            layer=super().getBaseLayer(),
        )
        super().addGameObject(backgroundImage)

    def updateGameObjects(self):
        super().drawByLayer()
        pygame.display.update()
        waitForKeyPress(pygame.K_RETURN)
