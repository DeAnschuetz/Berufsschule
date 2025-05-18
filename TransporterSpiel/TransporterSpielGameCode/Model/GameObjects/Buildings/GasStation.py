import pygame

from Model.GameObjects.Buildings.Building import Building
from Services.ConfigService import getConfig


class GasStation(Building):

    def __init__(self, image : pygame.Surface, screen : pygame.Surface, xCoordinate : float = 0.0, yCoordinate : float = 0.0):
        gasStationConfig = getConfig().getGameConfig().getGasStationConfig()
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=False,
            image=image,
            screen=screen,
            totalResourceStored=0.0,
            transferRate=gasStationConfig.getTransferRate()
        )
        # Increase Collision Radius of the GasStation to make Refueling easier
        super().setCollisionRadius(super().getCollisionRadius() * 1.5)

    def giveResource(self) -> float:
        return self.__transferRate__

