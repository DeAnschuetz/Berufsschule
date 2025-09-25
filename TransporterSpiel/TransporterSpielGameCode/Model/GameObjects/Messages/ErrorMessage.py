import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Services.ConfigService import getConfig
from Services.PygameService import waitForKeyPress

class ErrorTextGameObject(GameObjectContainer):
    """
    A Class representing an Error Text Display with a main Message and Footer.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer) to manage contained GameObjects.
    """

    def __init__(self, screen: pygame.Surface, message: str, baseLayer: int = -1000):
        """
        Initialize an ErrorTextGameObject Instance.

        Args:
            screen (pygame.Surface): The Pygame surface to draw the error message on.
            message (str): The main error message text.
            baseLayer (int): The rendering base layer; lower values draw underneath other objects.
        """
        config = getConfig()
        errorMessageConfig = config.getErrorMessageConfig()
        footerMessage: str = errorMessageConfig.getFooterMessage()
        errortextSize: int = errorMessageConfig.getErrorTextSize()
        footerFontSize: int = errorMessageConfig.getFooterFontSize()
        footerFontColor: list[int] = errorMessageConfig.getFooterFontColor()
        messageFontColor: list[int] = errorMessageConfig.getMessageFontColor()

        super().__init__(
            screen=screen,
            baseLayer=baseLayer
        )

        #  Create the Error Message Text
        errorMessage = TextGameObject(
            message=message,
            xCoordinate=screen.get_width() / 2,
            yCoordinate=screen.get_height() / 2,
            fontSize=errortextSize,
            screen=screen,
            color=(messageFontColor[0], messageFontColor[1], messageFontColor[2]),
            layer=baseLayer
        )
        self.addGameObject(errorMessage)

        # Create the Error Message Footer
        errorFooter = TextGameObject(
            message=footerMessage,
            xCoordinate=screen.get_width() / 2,
            yCoordinate=screen.get_height() / 2 + errorMessage.getHeight(),
            fontSize=footerFontSize,
            screen=screen,
            color=(footerFontColor[0], footerFontColor[1], footerFontColor[2]),
            layer=baseLayer
        )
        self.addGameObject(errorFooter)

    def draw(self):
        """
        Update and Draw the Error Message and Footer.

        This method clears the screen, draws all contained GameObjects by their layer,
        updates the display, and waits for the user to press the RETURN key before continuing.
        """
        # Dark background for Error display
        self.__screen__.fill((30, 30, 30))
        super().draw()

        # Update the entire Display with new drawings
        pygame.display.update()
        # Pause here until the User presses the RETURN key
        waitForKeyPress(pygame.K_RETURN)