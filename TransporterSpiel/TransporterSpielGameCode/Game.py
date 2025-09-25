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

class Game:
    """
    A Class representing the Main Game Loop and Setup for the Vehicle Game.

    Attributes:
        __difficulty__ (GameDifficulty): The Difficulty Level for the current Game Round.
        __playing__ (bool): Flag indicating whether the Game is currently being played.
        __running__ (bool): Flag indicating whether the Game Loop is running.
        __oreDelivered__ (float): The Amount of Ore delivered during the Game.
        __screen__ (pygame.Surface): The Pygame Surface representing the Game Window.
        __mainMenu__ (MainMenu): The Main Menu Interface.
        __clock__ (pygame.time.Clock): Clock for managing the Frame Rate.
        __difficultySelectionService__ (DifficultySelectionService): Service to manage Difficulty Selection.
        __gameObjectCreationService__ (GameObjectCreationService): Service to create Game Objects.
        __windowHeight__ (int): Height of the Game Window.
        __gameWidth__ (int): Width of the actual Game Area (excluding HUD).
        __hudWidth__ (int): Width of the HUD Sidebar.
        __difficultySelected__ (bool): Whether the Difficulty Selection Screen should be shown.
        __fps__ (int): The Frames Per Second Limit for the Game.
    """
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
    __difficultySelected__ : bool
    __fps__ : int


    def __init__(self):
        """
        Initialize the Game Environment, including Window Setup, Services, and Menu Components.
        """
        config = getConfig()
        screenConfig = config.getScreenConfig()
        windowWidth = screenConfig.getScreenWidth()
        self.__hudWidth__ = screenConfig.getHudConfig().getSideHudConfig().getWidth()
        self.__gameWidth__ = windowWidth - self.__hudWidth__
        self.__windowHeight__ = screenConfig.getScreenHeight()
        self.__difficultySelected__ = config.getDifficultySelection()
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
        """
        Display an Error Message on the Game Screen.

        Args:
            message (str): The Error Message Text to be displayed.
        """
        errorMessage : ErrorTextGameObject =ErrorTextGameObject(
            self.__screen__,
            message,
        )
        errorMessage.draw()

    def __waitForKeyPress__(self, key):
        """
        Wait until the given Key is pressed or the Window is closed.

        Args:
            key (int): Pygame Key Code to wait for.

        Returns:
            bool: True if the specified Key was pressed, False if the Window was closed.
        """
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
        """
        Handle the Difficulty Selection Process.

        Returns:
            bool: True if a Difficulty was successfully selected, False if the Game should exit.
        """
        self.__oreDelivered__ = 0
        if self.__difficultySelected__:
            self.__difficulty__ = self.__difficultySelectionService__.selectDifficulty()
        else:
            # Create Difficulty with Default Values
            self.__difficulty__ = GameDifficulty()

        if self.__difficulty__ is None:
            return False
        return True

    def __run__(self):
        """
        Execute the Main Game Loop, handling Difficulty Selection and Round Execution.
        """
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

            # Game Loop for the Current Round
            while currentRound.isPlaying():

                self.__clock__.tick(self.__fps__)

                currentRound.update()


        pygame.quit()

# Handle external screen argument
useSmallScreenOuter = "--small" in sys.argv

# Load Configuration before Game Initialization
loadConfig(useSmallScreenOuter)

# Start the Game
game = Game()