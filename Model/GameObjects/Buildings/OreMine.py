# OreMine.py
import pygame
from Model.GameObjects.Buildings.Building import Building
from Services.ConfigService import getConfig


class OreMine(Building):

    def __init__(self, image: pygame.Surface, screen: pygame.Surface, xCoordinate: float = 0, yCoordinate: float = 0, totalOre: int = 1000) -> None:
        oreMineConfig = getConfig().getGameConfig().getOreMineConfig()
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=False,
            image=image,
            layer=1,
            screen=screen,
            totalResourceStored=totalOre,
            transferRate=oreMineConfig.getTransferRate()
        )