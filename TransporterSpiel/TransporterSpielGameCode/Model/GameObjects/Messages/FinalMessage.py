import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Services.PygameService import waitForKeyPress
from Services.ConfigService import getConfig

class FinalTextGameObject(GameObjectContainer):
    """
    A Class to Display a Centered Final Text Message with a Footer Prompt and Background.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer) which manages multiple GameObjects.
    """
    def __init__(
            self,
            screen: pygame.Surface,
            message: str,
            isWinMessage: bool,
            borderSize: int = 30,
            backgroundColor: tuple[int, int, int]  = (50, 50, 50)
    ):
        """
        Initialize the FinalTextGameObject with message, footer, and background.

        Args:
            screen (pygame.Surface): The Surface to draw the message on.
            message (str): The main message text to display.
            borderSize (int): Padding size around the text inside background.
        """
        super().__init__(
            screen=screen,
            baseLayer=100000
        )
        config = getConfig()
        finalMessageConfig = config.getFinalMessageConfig()
        footerMessage: str = finalMessageConfig.getFooterMessage()
        finalMessageSize: int = finalMessageConfig.getErrorTextSize()
        footerFontSize: int = finalMessageConfig.getFooterFontSize()
        footerFontColor: list[int] = finalMessageConfig.getFooterFontColor()
        messageFontColorWin: list[int] = finalMessageConfig.getMessageFontColorWin()
        messageFontColorLoose: list[int] = finalMessageConfig.getMessageFontColorWin()
        messageColor: list[int]
        if isWinMessage:
            messageColor = messageFontColorWin
        else:
            messageColor = messageFontColorLoose

        # Create Main Message TextGameObject centered on screen
        finalMessage = TextGameObject(
            message=message,
            xCoordinate=screen.get_width() // 2,
            yCoordinate=screen.get_height() // 2,
            fontSize=finalMessageSize,
            screen=screen,
            color=(messageColor[0], messageColor[1], messageColor[2]),
            layer=super().getBaseLayer() + 1,
        )
        super().addGameObject(finalMessage)

        # Create Footer TextGameObject positioned below the main message
        footer = TextGameObject(
            message=footerMessage,
            xCoordinate=screen.get_width() // 2,
            yCoordinate=screen.get_height() // 2 + finalMessage.getHeight() + 10,
            fontSize=footerFontSize,
            screen=screen,
            color=(footerFontColor[0], footerFontColor[1], footerFontColor[2]),
            layer=super().getBaseLayer() + 1,
        )
        super().addGameObject(footer)

        # Create Background Surface filled with background color
        backgroundWidth = max(finalMessage.getWidth(), footer.getWidth()) + borderSize
        backgroundHeight = finalMessage.getHeight() + footer .getHeight() + 10 + borderSize
        backgroundImageSurface : pygame.Surface = pygame.Surface((backgroundWidth, backgroundHeight))
        backgroundImageSurface.fill(backgroundColor)

        # Create Background ImageGameObject centered slightly below screen center
        backgroundImage: ImageGameObject = ImageGameObject(
            screen=screen,
            xCoordinate=screen.get_width() // 2,
            yCoordinate=screen.get_height() // 2 + 10,
            image=backgroundImageSurface,
            layer=super().getBaseLayer(),
        )
        super().addGameObject(backgroundImage)

    def draw(self):
        """
        Draw the Background, Main Message, and Footer on screen,
        then wait until the user presses the ENTER key to continue.
        """
        super().draw()
        pygame.display.update()
        waitForKeyPress(pygame.K_RETURN)