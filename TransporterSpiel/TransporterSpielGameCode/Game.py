import os

import pygame
import sys

from Model.GameObjects.Game.GameRound import GameRound
from Model.GameObjects.Messages.ErrorMessage import ErrorTextGameObject
from Model.GameObjects.Game.GameDifficulty import GameDifficulty
from Model.GameObjects.MenuElements.MainMenu import MainMenu
from Model.GameObjects.Exceptions.QuitException import QuitException
from Services.ConfigService import loadConfig, getConfig
from Services.DifficultySelectionService import DifficultySelectionService
from Services.GameObjectCreationService import GameObjectCreationService


def loadImg(baseDir, fileName, size):
    image = pygame.image.load(os.path.join(baseDir, "Assets", fileName)).convert_alpha()
    image = pygame.transform.scale(image, size)
    image.set_colorkey((255, 255, 255))
    return image


class Game:
    __difficulty__ : GameDifficulty
    __playing__ : bool
    __running__ : bool

    __oreDelivered__ : float
    __screen__ : pygame.Surface

    __mainMenu__ : MainMenu
    __clock__ : pygame.time.Clock
    __difficultySelectionService__ : DifficultySelectionService
    __gameObjectCreationService__ : GameObjectCreationService

    __windowHeight__ : int
    __gameWidth__ : int
    __hudWidth__ : int
    __difficultySelection__ : bool
    __fps__ : int


    def __init__(self):
        config = getConfig()
        screenConfig = config.getScreenConfig()
        windowWidth = screenConfig.getScreenWidth()
        self.__hudWidth__ = screenConfig.getHudConfig().getSideHudConfig().getWidth()
        self.__gameWidth__ = windowWidth - self.__hudWidth__
        self.__windowHeight__ = screenConfig.getScreenHeight()
        self.__difficultySelection__ = config.getDifficultySelection()
        self.__fps__ = config.getFPS()

        pygame.init()
        self.__screen__ = pygame.display.set_mode((windowWidth, self.__windowHeight__))
        pygame.display.set_caption("Vehicle Game")

        self.__clock__ = pygame.time.Clock()

        self.__paused__ = False
        self.__running__ = True
        self.__oreDelivered__ = 0

        self.__gameObjectCreationService__ = GameObjectCreationService(
            self.__screen__,
            self.__gameWidth__,
            self.__windowHeight__
        )
        # Setup Main Menu
        self.__mainMenu__ = MainMenu(
            screen=self.__screen__,
            bigFont=32,
            smallFont=22
        )

        self.__difficultySelectionService__ = DifficultySelectionService(
            screen=self.__screen__,
            clock=self.__clock__
        )

        self.__run__()

    def __showErrorMessage__(self, message):
        errorMessage : ErrorTextGameObject =ErrorTextGameObject(
            self.__screen__,
            message,
        )
        errorMessage.updateGameObjects()

    def __waitForKeyPress__(self, key):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running__ = False

                if event.type == pygame.KEYDOWN:
                    if event.key == key:
                        return True
        return False

    def __selectDifficulty__(self):
        self.__oreDelivered__ = 0
        if self.__difficultySelection__:
            self.__difficulty__ = self.__difficultySelectionService__.selectDifficulty()
        else:
            self.__difficulty__ = GameDifficulty()

        if self.__difficulty__ is None:
            return False
        return True

    def __run__(self):
        self.__running__ = True
        while self.__running__:
            try:
                if not self.__selectDifficulty__():
                    break
            except QuitException:
                self.__running__ = False
                break

            self.__playing__ = True
            currentRound : GameRound = GameRound(
                difficulty=self.__difficulty__,
                gameObjectCreationService=self.__gameObjectCreationService__,
                mainMenu=self.__mainMenu__,
                screen=self.__screen__
            )
            while currentRound.isPlaying():

                self.__clock__.tick(self.__fps__)
                # TODO WEnn noch Zeit bewegung auf DeltaTime
                #deltaTime = self.__clock__.tick(60) / 1000.0

                currentRound.update()


        pygame.quit()

useSmallScreenOuter = "--small" in sys.argv
# Load config once
loadConfig(useSmallScreenOuter)
game = Game()