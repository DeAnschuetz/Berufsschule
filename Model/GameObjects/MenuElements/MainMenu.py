import pygame

from Model.GameObjects.Base.GameObjectContainer import GameObjectContainer
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Messages.TextGameObject import TextGameObject


class MainMenu(GameObjectContainer):
    __isActive__: bool

    def __init__(self, screen : pygame.Surface, bigFont : int, smallFont : int):
        windowWidth : int = screen.get_width()
        windowHeight: int = screen.get_height()
        menuBackground: pygame.Surface = pygame.Surface((windowWidth, windowHeight))
        menuBackground.set_alpha(180)
        menuBackground.fill((20, 20, 20))
        startOffset : int = windowHeight // 2
        offset : int = startOffset
        super().__init__(
            screen=screen,
            baseLayer=1000,
            xCoordinate=windowWidth // 2,
            yCoordinate=offset
        )
        self.__menuItems__ = []
        textMenuItems: list[TextGameObject] = []
        imageMenuItems: list[ImageGameObject] = []
        background = ImageGameObject(
            screen=screen,
            collision=False,
            layer=super().getBaseLayer() + 2,
            xCoordinate=super().getXCoordinate(),
            yCoordinate=super().getYCoordinate(),
            image=menuBackground
        )
        imageMenuItems.append(background)
        mainMenuMessage : TextGameObject = TextGameObject(
            message="Paused",
            identifier="%mainMenuHeader%",
            xCoordinate=super().getXCoordinate(),
            fontSize=bigFont,
            yCoordinate=super().getYCoordinate(),
            screen=screen,
            layer=super().getBaseLayer() + 2,
        )
        textMenuItems.append(mainMenuMessage)
        offset = offset + mainMenuMessage.getImage().get_height() + 40

        mainMenuMessage : TextGameObject = TextGameObject(
            message="Press ESC to Resume",
            xCoordinate=super().getXCoordinate(),
            yCoordinate=offset,
            fontSize=smallFont,
            screen=screen,
            layer=super().getBaseLayer() + 2,
        )
        textMenuItems.append(mainMenuMessage)
        offset = offset + mainMenuMessage.getImage().get_height() + 10

        mainMenuMessage : TextGameObject = TextGameObject(
            message="Press R to Restart",
            xCoordinate=super().getXCoordinate(),
            yCoordinate=offset,
            fontSize=smallFont,
            screen=screen,
            layer=super().getBaseLayer() + 2,
        )
        textMenuItems.append(mainMenuMessage)
        offset = offset + mainMenuMessage.getImage().get_height() + 10

        mainMenuMessage : TextGameObject = TextGameObject(
            message="Press Q to Quit",
            xCoordinate=super().getXCoordinate(),
            yCoordinate=offset,
            fontSize=smallFont,
            screen=screen,
            layer=super().getBaseLayer() + 2,
        )
        textMenuItems.append(mainMenuMessage)

        offset = offset + mainMenuMessage.getImage().get_height() + 10
        totalHeight : int = sum(message.getImage().get_height() for message in textMenuItems)
        maxWidth = max(message.getImage().get_width() for message in textMenuItems)
        menuBox: pygame.Surface = pygame.Surface((maxWidth + 20, offset - startOffset + 20))
        menuBox.set_alpha(180)
        menuBox.fill((80, 80, 80))

        menuBoxObject : ImageGameObject = ImageGameObject(
            screen=screen,
            collision=False,
            layer=super().getBaseLayer() + 1,
            xCoordinate=windowWidth // 2,
            yCoordinate=windowHeight // 2 + totalHeight - 15,
            image=menuBox
        )

        imageMenuItems.append(menuBoxObject)
        super().setGameObjects(imageMenuItems + textMenuItems)
        self.__isActive__ = False

    def close(self):
        """Deactivate the Main Menu."""
        self.__isActive__ = False

    def updateGameObjects(self):
        """"Draw all the MenuItems if it is active."""
        if self.__isActive__:
            super().drawByLayer()

    def open(self):
        """Activate the Main Menu."""
        self.__isActive__ = True