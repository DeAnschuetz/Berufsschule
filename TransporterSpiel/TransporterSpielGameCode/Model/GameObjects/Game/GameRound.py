import sys
from typing import cast

import pygame

from Model.GameObjects.Base.GameObject import GameObject
from Model.GameObjects.Game.GameDifficulty import GameDifficulty
from Model.GameObjects.Buildings.GasStation import GasStation
from Model.GameObjects.Vehicles.Helicopter import Helicopter
from Model.GameObjects.Messages.FinalMessage import FinalTextGameObject
from Model.GameObjects.Messages.TimedMessage import TimedTextGameObject
from Model.GameObjects.Buildings.OreMine import OreMine
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Model.GameObjects.Buildings.OreUnloadStation import OreUnloadStation
from Model.GameObjects.MenuElements.Hud import Hud
from Model.GameObjects.MenuElements.MainMenu import MainMenu
from Services.ConfigService import getConfig
from Services.GameObjectCreationService import GameObjectCreationService


class GameRound:
    """
    A Class representing a single Round of the Game.

    Attributes:
        __gameObjects__ (list[GameObject]): List of all active Game Objects.
        __screen__ (pygame.Surface): Game Surface where Objects are drawn.
        __paused__ (bool): Flag indicating whether the Game is paused.
        __oreDelivered__ (float): Amount of Ore delivered so far.
        __oreToCollect__ (float): Total Ore required to win.
        __gameWidth__ (int): Width of the active Game Area.
        __gameHeight__ (int): Height of the Game Screen.
        __playing__ (bool): Flag indicating if the Game is running.
        __difficulty__ (GameDifficulty): Difficulty Settings of the Game.
        __interactionCheckCounter__ (int): Counter to control frequency of interaction checks.
    """
    __gameObjects__ : list[GameObject]
    __screen__ : pygame.Surface
    __paused__ : bool
    __oreDelivered__ : float
    __oreToCollect__ : float
    __gameWidth__ : int
    __gameHeight__ : int
    __playing__ : bool
    __difficulty__ : GameDifficulty
    __interactionCheckCounter__: int

    def __init__(self, difficulty : GameDifficulty, gameObjectCreationService : GameObjectCreationService, mainMenu : MainMenu, screen : pygame.Surface):
        """
        Initialize a GameRound Object.

        Args:
            difficulty (GameDifficulty): Difficulty Configuration.
            gameObjectCreationService (GameObjectCreationService): Service to create Game Objects.
            mainMenu (MainMenu): Main Menu Game Object.
            screen (pygame.Surface): Screen Surface for rendering.
        """
        screenConfig = getConfig().getScreenConfig()
        windowWidth: int = screenConfig.getScreenWidth()
        hudWidth: int = screenConfig.getHudConfig().getSideHudConfig().getWidth()
        self.__gameWidth__ = windowWidth - hudWidth
        self.__gameHeight__ = screenConfig.getScreenHeight()

        self.__gameObjects__ = gameObjectCreationService.createGameObjects(difficulty)
        self.__difficulty__ = difficulty
        self.__screen__ = screen
        self.__paused__ = False
        self.__oreDelivered__ = 0.0
        self.__oreToCollect__ = difficulty.getOreToCollect()
        self.__playing__ = True
        self.__hud__ = Hud(
            screen=screen,
            oreToCollect=difficulty.getOreToCollect(),
            gameObjects=self.__gameObjects__
        )

        # Make sure the Main Menu is closed at the Beginning
        mainMenu.close()
        self.__gameObjects__.append(mainMenu)
        self.__interactionCheckCounter__ = 0

    def isPlaying(self) -> bool:
        return self.__playing__

    def update(self):
        """
        Update the Game Round including Input, Collisions, Game Logic and Rendering.
        """
        self.__handleGameInput__()
        if not self.__paused__:
            oreTransport = cast(OreTransport, self.__filterGameObjects__(OreTransport))
            helicopter = cast(Helicopter, self.__filterGameObjects__(Helicopter))
            gasStation = cast(GasStation, self.__filterGameObjects__(GasStation))
            oreMine = cast(OreMine, self.__filterGameObjects__(OreMine))
            oreUnloadStation = cast(OreUnloadStation, self.__filterGameObjects__(OreUnloadStation))

            self.__handleCollisions__(
                oreTransport=oreTransport,
                helicopter=helicopter,
                gasStation=gasStation,
                oreMine=oreMine,
                oreUnloadStation=oreUnloadStation
            )

        self.__updateGameScreen__()

    def __isOreGoalReached__(self):
        """
        Check whether the Goal for Ore Delivery has been reached.

        Returns:
            bool: True if Goal is reached, else False.
        """
        if self.__oreDelivered__ >= self.__oreToCollect__:
            return True
        return False

    def __filterGameObjects__(self, typeToFilterFor):
        """
        Filter for a single Object of a given Type from all Game Objects.

        Args:
            typeToFilterFor (Type): The Type to filter for.

        Returns:
            GameObject | None: The first matching Object or None.
        """
        return next(filter(lambda obj: isinstance(obj, typeToFilterFor), self.__gameObjects__), None)

    def __checkGameStatus__(self):
        """
        Check the Game Status and append a Final Message if Game ends.
        """
        if self.__isOreGoalReached__():
            finalMessage : FinalTextGameObject = FinalTextGameObject(
                screen=self.__screen__,
                message="Congratulations, you have reached the ore goal!",
                backgroundColor=(10, 50, 10),
                isWinMessage=True
            )
            self.__gameObjects__.append(finalMessage)

        elif not self.__isGameWinnable__():
            finalMessage : FinalTextGameObject = FinalTextGameObject(
                screen=self.__screen__,
                message="Game over! The game is no longer winnable.",
                backgroundColor=(50, 10, 10),
                isWinMessage=False
            )
            self.__gameObjects__.append(finalMessage)

    def __isGameWinnable__(self):
        """
        Check whether it is still possible to win the Game.

        Returns:
            bool: True if Game is Winnable, else False.
        """
        oreTransport: OreTransport = cast(OreTransport, self.__filterGameObjects__(OreTransport))
        oreMine: OreMine = cast(OreMine, self.__filterGameObjects__(OreMine))

        # Check if OreTransport can still deliver enough Ore
        if oreTransport.getLoadedOreAmount() + oreMine.getTotalResourceStored() + self.__oreDelivered__ < self.__oreToCollect__:
            return False
        # Check if OreTransport has Fuel left
        if oreTransport.getFuelLevel() == 0.00:
            return False
        return True

    def __updateGameScreen__(self):
        """
        Update and Render the complete Game Screen.
        """
        self.__screen__.fill((10, 40, 10))
        self.__checkGameStatus__()
        self.__hud__.__updateGameObjects__()
        self.__renderGameObjects__()

    def __renderGameObjects__(self):
        """
        Render all Game Objects based on Layer and update the Display Buffer.
        """
        # Sort by layer
        self.__gameObjects__.sort(key=lambda obj: obj.getLayer())
        updatedGameObjects : list[GameObject] = []
        # Draw in order
        for gameObject in self.__gameObjects__:
            if isinstance(gameObject, FinalTextGameObject):
                gameObject.draw()
                self.__playing__ = False
                return

            # Only Update non MainMenu Game Objects if the Game is not paused
            if type(gameObject) is not MainMenu:
                if not self.__paused__:
                    gameObject.update()

            if isinstance(gameObject, TimedTextGameObject):
                if gameObject.isExpired():
                    continue

            gameObject.draw()
            updatedGameObjects.append(gameObject)

        # Replace GameObjects list with filtered updated list
        self.__gameObjects__ = updatedGameObjects

        # Update the Display Buffers
        pygame.display.update()

    def __handleGameInput__(self):
        """
        Handle Player Input Events such as Keyboard Presses and Quitting.
        """
        oreTransport : OreTransport = next(filter(lambda obj: isinstance(obj, OreTransport), self.__gameObjects__), None)
        if type(oreTransport) is None:
            return
        mainMenu :MainMenu = next(filter(lambda obj: isinstance(obj, MainMenu), self.__gameObjects__), None)
        if type(mainMenu) is None:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running__ = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    if self.__paused__:
                        mainMenu.close()
                        self.__paused__ = False
                    else:
                        mainMenu.open()
                        self.__paused__ = True

                if self.__paused__:
                    if event.key == pygame.K_r:
                        self.__playing__ = False
                        self.__paused__ = False
                    if event.key == pygame.K_q:
                        self.__playing__ = False
                        self.__running__ = False
                        pygame.quit()
                        sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            oreTransport.steer("right")
        if keys[pygame.K_d]:
            oreTransport.steer("left")
        if keys[pygame.K_w]:
            oreTransport.accelerate()
        if keys[pygame.K_s]:
            oreTransport.decelerate()

    def __handleCollisions__(self, oreTransport: OreTransport, helicopter : Helicopter, gasStation: GasStation, oreMine : OreMine, oreUnloadStation: OreUnloadStation):
        """
        Handle all Collision-based Interactions between Vehicles and Stations.

        Args:
            oreTransport (OreTransport): The Ore Transport Vehicle.
            helicopter (Helicopter): The Helicopter attempting to steal Ore.
            gasStation (GasStation): The Gas Station for refueling.
            oreMine (OreMine): The Ore Mine to load Ore from.
            oreUnloadStation (OreUnloadStation): The Station to unload Ore to.
        """
        # Check for collisions with walls
        if oreTransport.getXCoordinate() < 0.0:
            oreTransport.handleCollisionWithWall('left')
        if oreTransport.getXCoordinate() + oreTransport.getWidth() > self.__gameWidth__:
            oreTransport.handleCollisionWithWall('right')
        if oreTransport.getYCoordinate() < 0.0:
            oreTransport.handleCollisionWithWall('top')
        if oreTransport.getYCoordinate() + oreTransport.getHeight() > self.__gameHeight__:
            oreTransport.handleCollisionWithWall('bottom')

        # Increment loop counter
        self.__interactionCheckCounter__ += 1
        # Only process interaction logic every 10 Frames/ Loops
        if self.__interactionCheckCounter__ % 10 == 0:
            # Check for Helicopter Interaction
            helicopterCounter: int
            if helicopter.areColliding(oreTransport, True) and not helicopter.getIsEscaping() and oreTransport.getLoadedOreAmount() > 0.0:
                stolenAmount : float = helicopter.stealOre(oreTransport)
                self.__gameObjects__.append(
                    TimedTextGameObject(
                        message=f"Helicopter Stole {stolenAmount} Ore",
                        xCoordinate=oreTransport.getXCoordinate(),
                        yCoordinate=oreTransport.getYCoordinate(),
                        fontSize=24,
                        screen=self.__screen__,
                        duration=3
                    )
                )

            # Check for GasStation Interaction
            if oreTransport.areColliding(gasStation, True) and not oreTransport.fuelIsFull():
                oreTransport.refuel(gasStation.giveResource())
                self.__gameObjects__.append(
                    TimedTextGameObject(
                        message="Refueled!",
                        xCoordinate=oreTransport.getXCoordinate(),
                        yCoordinate=oreTransport.getYCoordinate(),
                        fontSize=24,
                        screen=self.__screen__,
                        duration=1
                    )
                )

            # Check for OreMine Interaction
            if oreMine.areColliding(oreTransport, True) and not oreTransport.oreIsFull():
                loaded = oreMine.giveResource()
                if loaded > 0:
                    surplus: float = oreTransport.loadOre(loaded)
                    oreMine.takeResource(surplus)
                    self.__gameObjects__.append(
                        TimedTextGameObject(
                            message=f"Loaded {loaded} Ore",
                            xCoordinate=oreTransport.getXCoordinate(),
                            yCoordinate=oreTransport.getYCoordinate(),
                            fontSize=24,
                            screen=self.__screen__,
                            duration=1
                        )
                    )

            # Check for OreUnloadStation Interaction
            if oreUnloadStation.areColliding(oreTransport, True) and not oreTransport.isEmpty():
                delivered = oreTransport.unloadOre(oreTransport.getLoadedOreAmount())
                oreUnloadStation.takeResource(delivered)
                self.__updateOreDelivered__(delivered)
                self.__gameObjects__.append(
                    TimedTextGameObject(
                        message=f"Delivered {delivered} Ore",
                        xCoordinate=oreTransport.getXCoordinate(),
                        yCoordinate=oreTransport.getYCoordinate(),
                        fontSize=24,
                        screen=self.__screen__,
                        duration=2
                    )
                )

            self.__interactionCheckCounter__ = 0

    def __updateOreDelivered__(self, amount):
        """
        Increase the Delivered Ore Count by the given Amount.

        Args:
            amount (float): Amount of Ore delivered.
        """
        self.__oreDelivered__ += amount