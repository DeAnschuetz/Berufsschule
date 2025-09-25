from typing import cast

import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject


class MainMenu(GameObjectContainer):
    """
    A Class representing the Main Menu overlay in the Game.

    Inherits from:
        GameObjectContainer (Model.GameObjects.Base.GameObjectContainer)

    Attributes:
        __isActive__ (bool): Indicates whether the Main Menu is currently active.
        __menuItems__ (list): A List of all the Text Menu Items.
    """
    __isActive__: bool

    def __init__(self, screen : pygame.Surface, bigFont : int, smallFont : int):
        """
        Initialize a MainMenu Object and build its visual layout.

        Args:
            screen (pygame.Surface): The Game Screen to draw the Menu on.
            bigFont (int): Font Size for the Header Text.
            smallFont (int): Font Size for the Menu Instructions.
        """
        #TODO auf Config ändern
        windowWidth : int = screen.get_width()
        windowHeight: int = screen.get_height()

        startOffset : int = windowHeight // 2
        offset : int = startOffset
        super().__init__(
            screen=screen,
            baseLayer=1000,
            xCoordinate=windowWidth // 2,
            yCoordinate=offset
        )

        # Semi-transparent background covering the whole screen
        menuBackground: pygame.Surface = pygame.Surface((windowWidth, windowHeight))
        menuBackground.set_alpha(180)
        menuBackground.fill((20, 20, 20))
        # Add dark background overlay
        self.__menuItems__ = []
        background = ImageGameObject(
            screen=screen,
            collision=False,
            layer=super().getBaseLayer() + 2,
            xCoordinate=super().getXCoordinate(),
            yCoordinate=super().getYCoordinate(),
            image=menuBackground
        )
        self.addGameObject(background)

        # Add main menu header
        mainMenuMessage : TextGameObject = TextGameObject(
            message="Paused",
            identifier="%mainMenuHeader%",
            xCoordinate=super().getXCoordinate(),
            fontSize=bigFont,
            yCoordinate=super().getYCoordinate(),
            screen=screen,
            layer=super().getBaseLayer() + 2,
        )
        self.addGameObject(mainMenuMessage)
        offset += mainMenuMessage.getImage().get_height() + 40

        # Add menu option texts
        for msg in ["Press ESC to Resume", "Press R to Restart", "Press Q to Quit"]:
            mainMenuMessage = TextGameObject(
                message=msg,
                xCoordinate=super().getXCoordinate(),
                yCoordinate=offset,
                fontSize=smallFont,
                screen=screen,
                layer=super().getBaseLayer() + 2,
            )
            self.addGameObject(mainMenuMessage)
            offset += mainMenuMessage.getImage().get_height() + 10

        # Calculate the size of the menu box
        totalHeight: int = 0
        messageWidths: list[int] = []
        for gameObject in self.__gameObjects__:
            textObject: TextGameObject = cast(TextGameObject, gameObject)
            totalHeight += textObject.getHeight()
            messageWidths.append(textObject.getWidth())
        maxWidth: int = max(messageWidths)

        offset = offset + mainMenuMessage.getImage().get_height() + 10
        menuBox: pygame.Surface = pygame.Surface((maxWidth + 20, offset - startOffset + 20))
        menuBox.set_alpha(180)
        menuBox.fill((80, 80, 80))

        # Add a box behind the menu items for better visibility
        menuBoxObject : ImageGameObject = ImageGameObject(
            screen=screen,
            collision=False,
            layer=super().getBaseLayer() + 1,
            xCoordinate=windowWidth // 2,
            yCoordinate=windowHeight // 2 + totalHeight - 15,
            image=menuBox
        )

        self.addGameObject(menuBoxObject)

        self.__isActive__ = False

    def open(self):
        """
        Activate the Main Menu.
        """
        self.__isActive__ = True

    def close(self):
        """
        Deactivate the Main Menu.
        """
        self.__isActive__ = False

    def draw(self):
        """"
        Draw all the MenuItems if it is active.
        """
        if self.__isActive__:
            super().draw()