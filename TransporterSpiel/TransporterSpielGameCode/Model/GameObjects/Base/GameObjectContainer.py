import pygame

from Model.GameObjects.Base.GameObject import GameObject

class GameObjectContainer(GameObject):
    """
    A Class representing a Container holding multiple Game Objects.

    Inherits from:
        GameObject (Model.GameObjects.Base.GameObject) to define Positioning and Layer for the Container.

    Attributes:
        __gameObjects__ (list[GameObject]): List of all contained Game Objects.
    """
    __gameObjects__: list[GameObject]

    def __init__(self, screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0, baseLayer: int = 0):
        """
        Initialize a GameObjectContainer Instance.

        Args:
            screen (pygame.Surface): Surface to draw the Container and its Game Objects on.
            xCoordinate (float): X-Coordinate of the Container.
            yCoordinate (float): Y-Coordinate of the Container.
            baseLayer (int): Base Layer for the Container.
        """
        super().__init__(
            screen=screen,
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            baseLayer=baseLayer
        )
        self.__gameObjects__ = []

    def getGameObjects(self) -> list[GameObject]:
        return self.__gameObjects__

    def setGameObjects(self, objects: list[GameObject]):
        self.__gameObjects__ = objects

    def addGameObject(self, imageObject: GameObject) -> None:
        """
        Add a new Game Object to the Container.

        Args:
            imageObject (GameObject): The Game Object to add.
        """
        self.__gameObjects__.append(imageObject)

    def removeGameObjectById(self, identifier: str) -> None:
        """
        Remove a Game Object from the Container based on its Identifier.

        Args:
            identifier (str): The Identifier of the Game Object to remove.
        """
        self.__gameObjects__ = [obj for obj in self.__gameObjects__ if obj.getIdentifier() != identifier]

    def getGameObjectById(self, identifier: str) -> GameObject:
        """
        Retrieve a Game Object by its Identifier.

        Args:
            identifier (str): The Identifier of the Game Object.

        Returns:
            GameObject: The Found Game Object or None if not found.
        """
        return next((obj for obj in self.__gameObjects__ if obj.getIdentifier() == identifier), None)

    def update(self) -> None:
        """
        Override Update to apply it to all contained Game Objects.
        """
        for gameObjets in self.__gameObjects__:
            gameObjets.update()

    def draw(self) -> None:
        """
        Sort Game Objects by their Layer and draw them.

        This ensures correct rendering Order based on Layer Depth.
        """
        self.__gameObjects__ = sorted(self.__gameObjects__, key=lambda item: item.getLayer())
        for gameObjets in self.__gameObjects__:
            gameObjets.draw()