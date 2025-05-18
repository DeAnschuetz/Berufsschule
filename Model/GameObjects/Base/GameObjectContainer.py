import pygame

from Model.GameObjects.Base.GameObject import GameObject

class GameObjectContainer(GameObject):

    __gameObjects__: list[GameObject]

    def __init__(self, screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0, baseLayer: int = 0):
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
        self.__gameObjects__.append(imageObject)

    def removeGameObjectById(self, identifier: str) -> None:
        self.__gameObjects__ = [obj for obj in self.__gameObjects__ if obj.getIdentifier() != identifier]

    def getGameObjectById(self, identifier: str) -> GameObject:
        return next((obj for obj in self.__gameObjects__ if obj.getIdentifier() == identifier), None)

    def updateGameObjects(self):
        for imageObject in self.__gameObjects__:
            imageObject.update()

    def drawByLayer(self) -> None:
        self.__gameObjects__ = sorted(self.__gameObjects__, key=lambda item: item.getLayer())
        for imageObject in self.__gameObjects__:
            imageObject.draw()

    def update(self) -> None:
        for imageObject in self.__gameObjects__:
            imageObject.update()

    def draw(self) -> None:
        self.__gameObjects__ = sorted(self.__gameObjects__, key=lambda item: item.getLayer())
        for imageObject in self.__gameObjects__:
            imageObject.draw()