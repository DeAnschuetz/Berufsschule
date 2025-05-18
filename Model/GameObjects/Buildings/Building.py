import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject

class Building(ImageGameObject):
    __transferRate__: float
    __totalResourceStored__ : float

    def __init__(self,image: pygame.Surface, screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0, collision: bool = False,  layer: int = 1, totalResourceStored : float = 0, transferRate: int = 100) -> None:
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=collision,
            image=image,
            layer=layer,
            screen=screen
        )
        self.__transferRate__ = transferRate
        self.__totalResourceStored__ = totalResourceStored

    def getTotalResourceStored(self) -> float:
        return self.__totalResourceStored__

    def giveResource(self) -> float:
        if self.__totalResourceStored__ <= 0:
            return 0
        amountTransferred =  min(self.__transferRate__, self.__totalResourceStored__)
        self.__totalResourceStored__ -= amountTransferred
        return amountTransferred

    def takeResource(self, transferredAmount : float) -> None:
        self.__totalResourceStored__ += transferredAmount